import boto3
from entidades.Cliente import Cliente

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def inativar(documento):
    cliente = Cliente(documento)
    cliente_resp = cliente.inativar(dynamodb)

    if not cliente_resp.__contains__('Erro:'):
        print("Cliente inativado com sucesso!")
    else:
        print(cliente_resp)


if __name__ == '__main__':
    inativar("11122255500")
