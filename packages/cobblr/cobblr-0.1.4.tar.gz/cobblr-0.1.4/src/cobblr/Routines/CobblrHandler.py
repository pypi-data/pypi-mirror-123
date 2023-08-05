import asyncio
import threading
import time
import zmq
from enum import Enum
from zmq.asyncio import Poller

from .CobblrRouter import CobblrRouter
from .CobblrDealer import CobblrDealer
from .CobblrPubSubProxy import CobblrPubSubProxy
from .CobblrPublish import CobblrPublish
from .CobblrSubscribe import CobblrSubscribe
from .CobblrHeartbeat import CobblrHeartbeat

from ..config import AppType, DEFAULT_PORT
from ..cobblr_debug import db_print
from ..cobblr_static_functions import zpipe, list_or_string_encode


class HandlerStates(Enum):
    READY = 0
    INIT = 1
    REGISTERING = 2
    REROUTING = 3
    CONNECTING = 4
    CREATE_ROUTER = 5
    CREATE_DEALER = 6
    SENDING = 7
    RECEIVING = 8
    SHUTDOWN = 9


MSG_PRIORITY = {b"SHUTDOWN": 0,
                b"REGISTER": 1,
                b"ROUTER_PORT": 1,
                b"CONNECT": 2,
                b"CONN_ACK": 2,
                b"RQ_ROUTE": 3,
                b"ACK_ROUTE": 4,
                b"GET_CONNS": 5,
                b"GET_MSG": 5,
                b"GET_SUB": 5,
                b"SUBSCRIBE": 5,
                b"SEND_TO": 6,
                b"MSG_FROM": 6,
                b"PUB_MSG": 6,
                }


class CobblrHandler:
    def __init__(self, queue, context, app_name, app_type, api_pipe):

        # register input objects
        self.context = context
        self.app_name = app_name
        self.app_type = app_type
        self.api_pipe = api_pipe

        # register CobblrRoutine objects
        self.queue = queue
        self.ongoing = True

        # placeholder router pipe
        self.router_pipe = None

        # placeholder poller
        self.poller = None

        # placeholder objects for pub-sub
        self.pubsub_listener = None
        self.pubsub_proxy = None
        self.publisher = None
        self.subscriber = None
        self.subscriber_pipe = None
        self.heartbeat = None

        # create internal housekeeping objects
        """
        NEEDS:
        Shift all these variables to a new addressbook object
        """
        self.dealers = {}
        self.dealer_threads = {}
        self.router = None
        self.ports = []
        self.has_router = False
        self.message_queue = []
        self.sub_message_queue = []
        self.alive = True
        self.handler_queue = asyncio.PriorityQueue()

        # create handler state object
        self.handler_state = HandlerStates.INIT

    async def start(self):
        await self.queue.put(self.run_first())

    async def run_method(self, method):
        if not self.ongoing:
            return 0
        await method()
        if self.ongoing:
            await self.queue.put(self.run_method(method))

    def end(self):
        if self.ongoing:
            self.ongoing = False
        else:
            db_print("task is already ending")

    async def run_first(self):

        db_print("run_first")
        # create router pipe
        self.router_pipe = zpipe(self.context)

        # create poller and register pipes
        self.poller = Poller()
        self.poller.register(self.api_pipe, zmq.POLLIN)

        if self.app_type == AppType.SERVICE_APP:
            await self.create_router(DEFAULT_PORT)
            # create a pub-sub proxy to run in a separate thread
            # implement a pipe to listen on this
            # self.pubsub_listener = zpipe(self.context)
            await self.create_pub_sub_proxy() # defaults to no listener pipe

        elif self.app_type == AppType.CLIENT_APP:
            await self.create_dealer("service", DEFAULT_PORT)
            self.ports.append(DEFAULT_PORT)
            # Although pub, sub and heartbeat are simpler in operation that request - response
            # we need async here because the context is an async context - it has to live on an event loop
            # this will help in adding more complex behaviour in the future
            # create a publisher
            await self.create_publisher()
            # create a subscriber
            await self.create_subscriber()
            # create a heartbeat
            await self.create_heartbeat()

        db_print("redefine")

        self.handler_state = HandlerStates.READY
        await self.queue.put(self.run_method(self.receive_messages))
        await self.queue.put(self.run_method(self.handle_messages))

    async def receive_messages(self):
        """
        waits on polling
        :return: no return
        """

        # db_print("receiver waiting \n")

        poll_in = await self.poller.poll()
        event = dict(poll_in)
        # db_print("polled - state = %s\n" % self.handler_state)

        if self.router_pipe[1] in event:
            message = await self.router_pipe[1].recv_multipart()
            db_print("router pipe recv: %s" % message)

            await self.handler_queue.put((MSG_PRIORITY[message[0]], ["router"] + [*message]))

        for key, dealer in list(self.dealers.items()):
            if dealer in event:
                message = await dealer.recv_multipart()
                db_print("dealer %s pipe recv: %s" % (key, message))

                await self.handler_queue.put((MSG_PRIORITY[message[0]], ["dealer", key] + [*message]))

        if self.api_pipe in event:
            message = await self.api_pipe.recv_multipart()

            # db_print("api pipe recv: %s" % message)

            await self.handler_queue.put((MSG_PRIORITY[message[0]], ["api"] + [*message]))

        if self.app_type == AppType.CLIENT_APP:
            if self.subscriber_pipe[1] in event:
                message = await self.subscriber_pipe[1].recv_multipart()
                db_print("sub msg recv: %s" % message)

                self.sub_message_queue.append(message)

    async def handle_messages(self):
        """
        waits on messages
        :return: no return
        """

        # db_print("handler waiting \n")
        # db_print("state = %s \n" % self.handler_state)

        # **********************
        # GET THE NEXT MESSAGE :
        # **********************

        (priority, message) = await self.handler_queue.get()

        # db_print("handler next message = %s with priority %s\n" % (message, priority))
        # db_print("state = %s \n" % self.handler_state)

        # *************************************
        # Messages to be handled in READY STATE
        # *************************************

        if self.handler_state == HandlerStates.READY:

            # ********************
            # Messages from ROUTER
            # ********************

            if message[0] == "router":
                message = message[1:]

                if message[0] == b"REGISTER":
                    db_print("registering?")
                    self.handler_state = HandlerStates.REGISTERING
                    dlr_name = message[1]
                    new_port = self.next_port()
                    await self.router_pipe[1].send_multipart([b"ROUTER_PORT", dlr_name, str.encode("%s" % new_port)])

                if message[0] == b"RQ_ROUTE":
                    dlr_name = message[1]
                    request = message[2]
                    port_num = message[3]
                    db_print("recv RQ_ROUTE: %s, %s, %s" % (dlr_name.decode(), request.decode(), port_num.decode()))
                    if self.app_type == AppType.CLIENT_APP:
                        db_print("RQ_ROUTE: client app")
                        if self.app_name == request.decode():
                            self.handler_state = HandlerStates.REROUTING
                            await self.create_dealer(dlr_name.decode(), port_num.decode())
                            await self.dealers[dlr_name.decode()].send_multipart([b"ACK_ROUTE",
                                                                                  str.encode("%s" % self.app_name),
                                                                                  str.encode("%s" % self.router.port)])
                        else:
                            db_print("Routing request: Error - cannot route via CLIENT_APP")
                    elif self.app_type == AppType.SERVICE_APP:
                        db_print("RQ_ROUTE: service app")
                        try:
                            await self.dealers[request.decode()].send_multipart(message)
                        except IndexError as e:
                            db_print("Error, dealer %s not found: %s" % (request, e))
                        except KeyError as e:
                            db_print("Error, dealer %s not found: %s" % (request, e))

                if message[0] == b"MSG_FROM":
                    self.message_queue.append(message[1:])

            # ************************
            # Messages from LOCAL PIPE
            # ************************

            if message[0] == "api":
                message = message[1:]

                if message[0] == b"SEND_TO":
                    to = message[1].decode()
                    await self.send_to(to, message[2:])

                if message[0] == b"PUB_MSG":
                    await self.publisher.pub(message[1], message[2:])

                if message[0] == b"SUBSCRIBE":
                    self.subscriber.sub(message[1])

                if message[0] == b"GET_CONNS":
                    con_dealer_list = []
                    for dlr_name in list(self.dealers.keys()):
                        con_dealer_list.append(str.encode(dlr_name))
                    await self.api_pipe.send_multipart([b"CONNS"] + con_dealer_list)

                if message[0] == b"GET_MSG":
                    number = len(self.message_queue)
                    if number == 0:
                        await self.api_pipe.send(b"NO_MSG")
                    else:
                        message = self.message_queue.pop()
                        await self.api_pipe.send_multipart([b"MSG"] + [str.encode("%s" % number)] + message)

                if message[0] == b"GET_SUB":
                    number = len(self.sub_message_queue)
                    if number == 0:
                        await self.api_pipe.send(b"NO_SUB")
                    else:
                        message = self.sub_message_queue.pop()
                        await self.api_pipe.send_multipart([b"SUB"] + [str.encode("%s" % number)] + message)

                if message[0] == b"REGISTER":
                    db_print("registering(handler)")
                    self.dealers["service"].send_multipart([b"REGISTER"])
                    self.handler_state = HandlerStates.REGISTERING

                if message[0] == b"RQ_ROUTE":
                    request = message[1]
                    rq_message = [b"RQ_ROUTE",
                                  str.encode("%s" % self.app_name),
                                  request,
                                  str.encode("%s" % self.router.port)]
                    if request.decode() in self.dealers:
                        db_print("api RQ dealer recv")
                        await self.dealers[request.decode()].send_multipart(rq_message)
                    elif self.app_type == AppType.SERVICE_APP:
                        db_print("Requested dealer is not known")
                    else:
                        db_print("api RQ service recv")
                        self.handler_state = HandlerStates.REROUTING
                        await self.dealers["service"].send_multipart(rq_message)

                if message[0] == b"SHUTDOWN":
                    self.alive = False

        # ************************
        # END OF ----- READY STATE
        # ************************

        # *******************************************
        # Messages to be handled in REGISTERING STATE
        # *******************************************

        elif self.handler_state == HandlerStates.REGISTERING:

            # ********************
            # Messages from ROUTER
            # ********************

            if message[0] == "router":
                message = message[1:]

                if message[0] == b"CONNECT":
                    db_print("connect: %s" % message)
                    dlr_name = message[1].decode()
                    port_num = int(message[2].decode())
                    await self.create_dealer(dlr_name, port_num)
                    await self.dealers[dlr_name].send_multipart([b"CONN_ACK"])
                    self.handler_state = HandlerStates.READY

                elif message[0] == b"CONN_ACK":
                    db_print("connected")
                    self.handler_state = HandlerStates.READY

            # ********************
            # Messages from DEALER
            # ********************

            elif message[0] == "dealer":
                dealer = self.dealers[message[1]]
                message = message[2:]

                if message[0] == b"ROUTER_PORT":
                    port_num = int(message[1].decode())
                    await self.create_router(port_num)
                    dealer.send_multipart([b"CONNECT", str.encode(self.app_name), str.encode("%s" % port_num)])

        # *******************************************
        # END OF ----- REGISTERING STATE
        # *******************************************

        # *******************************************
        # Messages to be handled in REROUTING STATE
        # *******************************************

        elif self.handler_state == HandlerStates.REROUTING:

            if message[0] == "router":
                message = message[1:]

                if message[0] == b"ACK_ROUTE":
                    db_print("router recv ACK ROUTE")
                    dlr_name = message[1].decode()
                    port_num = message[2].decode()
                    if dlr_name in self.dealers:
                        db_print("route connection acknowledged")
                        self.handler_state = HandlerStates.READY
                    else:
                        await self.create_dealer(dlr_name, port_num)
                        await self.dealers[dlr_name].send_multipart([b"ACK_ROUTE",
                                                                     str.encode("%s" % self.app_name),
                                                                     str.encode("NULL")])
                        self.handler_state = HandlerStates.READY

                elif message[0] == b"CONN_ACK":
                    db_print("connected")
                    self.handler_state = HandlerStates.READY

        # *******************************************
        # END OF ----- REROUTING STATE
        # *******************************************

        # *************************************************
        # UNHANDLED messages go back onto the HANDLER QUEUE
        # *************************************************

        else:
            await self.handler_queue.put((priority, message))

    # *************************************************
    # Create a router object
    # *************************************************

    async def create_router(self, port):
        if self.has_router:
            db_print("router already exists")
            return 1
        else:
            self.router = CobblrRouter(self.queue, self.context, self.app_name, port, self.router_pipe[0])
            await self.router.start()
            self.ports.append(port)
            self.has_router = True
            self.poller.register(self.router_pipe[1], zmq.POLLIN)

    async def create_dealer(self, dlr_name, port):
        db_print("creating dealer %s in app %s on port %s" % (dlr_name, self.app_name, port))
        dealer_pipe = zpipe(self.context)
        self.dealers[dlr_name] = dealer_pipe[1]
        # now, technically the dealer threads aren't real threads
        # that's why we are using async - otherwise for N interconnected apps you have N squared threads
        # which could get messy quickly
        self.dealer_threads[dlr_name] = CobblrDealer(self.queue, self.context, self.app_name, port, dealer_pipe[0])
        await self.dealer_threads[dlr_name].start()
        self.poller.register(dealer_pipe[1], zmq.POLLIN)

    async def create_subscriber(self):
        if not self.subscriber:
            self.subscriber_pipe = zpipe(self.context)
            self.subscriber = CobblrSubscribe(self.context, self.queue, self.subscriber_pipe[0])
            await self.subscriber.start()
            self.poller.register(self.subscriber_pipe[1], zmq.POLLIN)
        else:
            db_print("Subscriber already exists!")

    async def create_publisher(self):
        if not self.publisher:
            self.publisher = CobblrPublish(self.context)
            await self.publisher.start()
        else:
            db_print("Publisher already exists")

    async def create_heartbeat(self):
        if not self.heartbeat:
            self.heartbeat = CobblrHeartbeat(self)
            await self.heartbeat.start()
        else:
            db_print("Heartbeat already exists")

    async def create_pub_sub_proxy(self, pipe=None):
        if not self.pubsub_proxy:
            self.pubsub_proxy = CobblrPubSubProxy(self.context, self.queue, pipe)
            await self.pubsub_proxy.start()
            if pipe:
                self.poller.register(pipe, zmq.POLLIN)
        else:
            db_print("pub_sub_proxy already exists")

    def next_port(self):
        port_num = DEFAULT_PORT
        while True:
            if self.ports.count(port_num) != 0:
                port_num += 1
            else:
                self.ports.append(port_num)
                return port_num

    async def publish_on(self, topic, message):
        out_msg = list_or_string_encode(message)
        out_topic = list_or_string_encode(topic)
        try:
            await self.publisher.pub(out_topic, out_msg)
        except zmq.ZMQError as e:
            db_print("zmq error: %s \n" % e)
            return 1

        return 0

    async def send_to(self, to, message):

        try:
            dealer = self.dealers[to]
        except KeyError as e:
            db_print("Invalid destination name %s" % e)
            return 1

        out_msg = list_or_string_encode(message)
        try:
            await dealer.send_multipart([b"SEND"] + out_msg)
        except zmq.ZMQError as e:
            db_print("zmq error: %s \n" % e)
            return 1

        return 0
