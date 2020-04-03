from greeter_server import serve
import greeter_client
import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def test_client(mocker):
    mocker_stub = mocker.patch(
        'greeter_client.helloworld_pb2_grpc.GreeterStub')
    mocker_say_hello = mocker_stub.return_value.SayHello
    mocker_say_hello.return_value.message = "Augi"
    mocker.patch(
        'greeter_client.grpc.insecure_channel')
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    greeter_client.grpc.insecure_channel.assert_called_once_with(
        'localhost:50051')
    call_greeter_stub = mocker_stub.call_count
    assert call_greeter_stub == 1
    mocker_say_hello.assert_called_once_with(
        helloworld_pb2.HelloRequest(name='you'))
    assert response.message == "Augi"


def test_server(mocker):
    mocker_server = mocker.patch('greeter_server.grpc.server')
    mocker_port = mocker_server.return_value.add_insecure_port
    mocker_start = mocker_server.return_value.start
    serve()
    call_server = mocker_server.call_count
    call_port = mocker_port.call_count
    mocker_port.assert_called_once_with('[::]:50051')
    mocker_start.assert_called_once_with()
    assert call_server == 1
    assert call_port == 1
