import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def remover(disco_id):
    disco = Disco()
    disco_resp = disco.remover(disco_id, dynamodb)

    if not disco_resp.__contains__('Erro:'):
        print("Disco removido com sucesso!")
    else:
        print(disco_resp)


if __name__ == '__main__':
    remover('6052f36d-b48b-11ec-b0fa-085bd6526d3f')
