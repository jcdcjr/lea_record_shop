import boto3
from entidades.Cliente import Cliente

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def obter_dados_cliente(documento):
    cliente = Cliente(documento)
    cliente_resp = cliente.obter_por_id(dynamodb)

    print(cliente_resp)


if __name__ == '__main__':
    obter_dados_cliente("11122233300")