import boto3
from entidades.Pedido import Pedido

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def listar_pedidos(documento, data_inicial, data_final):
    pedido = Pedido()
    pedido_resp = pedido.listar_pedidos(documento, data_inicial, data_final, dynamodb)

    print(pedido_resp)


if __name__ == '__main__':
    listar_pedidos(None, None, None)
