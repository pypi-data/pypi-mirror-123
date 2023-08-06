# Socket Api 2

This make easier to create servers and clients with socket.

Supported language is python 3. (Package wrote in 3.9.6)

## Installation

Use this command:

    pip install socket-api2

## Change Log

0.0.8 (13/10/2021)
-------------------
- Optimized

## Examples

Difference between SEND_METHOD.default_send and SEND_METHOD.just_send, with the default send the program send a lenght of the message then send the message to know how many bytes we need to receive, but the just_send is just send the message. 

Example for Server:

    from socket_api2 import *

    server = Server(ip="auto", port=5555)

    @server.on_client_connect()
    def handling_client(client):
        while True:
            if client.is_connected:
                msg = client.recv(2048)
                if msg == "hi":
                    client.send("hi 2", method=SEND_METHOD.default_send)
                
                elif msg == "I love u":
                    client.send("I love u too")

                else:
                    client.send("no hi", method=SEND_METHOD.just_send)
            else:
                break

    server.start()

Example for Client:

    from socket_api2 import *

    client = Client(target_ip="IP", target_port=5555, timeout=10)
    resp = client.connect()
    if 200:
        client.send("hi")
        client.recv(2048)

        client.send("I love u", method=SEND_METHOD.just_send)
        client.recv(2048)
    else:
        outstr("ERROR", "Something went wrong...")