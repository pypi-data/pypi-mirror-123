# cobblr

This is a package for simple client-broker and client-client communications 
using the [ZeroMQ](https://zeromq.org/) package for python.

It is designed for M2M communications and easy passing of data between
software modules. Each client program runs asynchronously in a single 
new background thread. Clients are addressed with a unique name and once
registered with a broker can request new communications.

This package was built as part of the [Digital Manufacturing on a Shoestring 
Project](https://www.digitalshoestring.net/).

This library is in development. 

Please check back soon!

## API

    from cobblr import CobblrBroker
    cb = CobblrBroker

Create and start a broker

    from cobblr import CobblrClient
    cl = CobblrClient("cl_test")

Create and start a client named `cl_test`

    cl.register()

Register client `cl_test` with the running broker

    from cobblr import CobblrClient
    cr = CobblrClient("cr_test")
    cr.register()

Create, start and register client `cr_test`

    cl.request_connection("cr_test")

Request a connection to client `cr_test` from client `cl_test`

    connection_list = cl.get_connected()

Populates `connection_list` with names of connected clients and broker. 
The broker is always named `service`.

    cl.send_message("cr_test",["string_1", "string_2"])

Sends a message from client `cl_test` to client `cr_test`, consisting of two 
strings.

    msg = ["no_msg"]
    while msg == ["no_msg"]:
        msg = cr.get_messages()
    print(msg)

Loop to read message inbox on client `cr_test`. Messages will be returned
as a list, with each entry a list of `[<message number>, <from address>, 
<message contents>]`.

The inbox is cleared on reading.

    cr.end

Ends client `cr_test`. **Not yet implemented!**

## Features List

- [x] Client name registration at broker
- [x] Single IP space
- [ ] Multiple IP and Network support
- [x] Request a connection to another named client
- [x] Request - Response messaging pattern between named clients
- [ ] Publish - Subscribe messaging pattern
- [x] Simple state machine with task prioritisation
- [x] Asynchronous background operation
- [ ] Smooth shutdown and restart
- [ ] Heartbeat for network status and awareness
- [ ] Backup broker
- [ ] Network configuration save and load
- [ ] Message encryption


