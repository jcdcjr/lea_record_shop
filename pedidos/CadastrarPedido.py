import boto3
from entidades.Pedido import Pedido

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def cadastrar(documento, disco_id, quantidade):
    pedido = Pedido()
    pedido_resp = pedido.cadastrar(documento, disco_id, quantidade, dynamodb)

    if not pedido_resp.__contains__('Erro:'):
        print("Pedido realizado com sucesso!")
    else:
        print(pedido_resp)


if __name__ == '__main__':
    cadastrar("11122233300", '60df5f62-b48b-11ec-8fec-085bd6526d3f', 1)
