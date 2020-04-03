import polynomial_server
from polynomial_server import serve
import polynomial_client
from polynomial_variable import value
import grpc
import polynomial_pb2
import polynomial_pb2_grpc


def test_server(mocker, monkeypatch):
    mocker_server = mocker.patch('polynomial_server.grpc.server')
    mocker_add_server = mocker.patch(
        'polynomial_server.polynomial_pb2_grpc.add_PolynomialServicer_to_server')
    mocker_add_insecure_port = mocker_server.return_value.add_insecure_port
    mocker_start_server = mocker_server.return_value.start
    mocket_termination_server = mocker_server.return_value.wait_for_termination
    monkeypatch.setattr(polynomial_server, "HOST", '2')
    serve()
    call_server = mocker_server.call_count
    call_add_server = mocker_add_server.call_count
    mocker_add_insecure_port.assert_called_once_with('[::]:2')
    mocker_start_server.assert_called_once_with()
    mocket_termination_server.assert_called_once_with()
    assert call_server == 1
    assert call_add_server == 1


def test_client(mocker):
    mocker_stub = mocker.patch(
        'polynomial_client.polynomial_pb2_grpc.PolynomialStub')
    mocker_solve = mocker_stub.return_value.Solve
    mocker_solve.return_value.res_x = [2, 2]
    mocker_solve.return_value.res_y = [10, 10]
    mocker_input = mocker.patch(
        'polynomial_client.polynomial_pb2.PolynomialInput')
    mocker.patch(
        'polynomial_client.grpc.insecure_channel')
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = polynomial_pb2_grpc.PolynomialStub(channel)
        for i in value:
            request = polynomial_pb2.PolynomialInput(x=i)
            response = stub.Solve(request)
    polynomial_client.grpc.insecure_channel.assert_called_once_with(
        'localhost:50051')
    call_stub = mocker_stub.call_count
    call_input = mocker_input.call_count
    call_solve = mocker_solve.call_count
    assert call_stub == 1
    assert call_input == len(value)
    assert call_solve == len(value)
    assert response.res_x == [2, 2]
    assert response.res_y == [10, 10]
