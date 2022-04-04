import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def repor_estoque(disco_id, quantidade):
    disco = Disco()
    disco_resp = disco.repor_estoque_disco(disco_id, quantidade, dynamodb)

    if not disco_resp.__contains__('Erro:'):
        print("Dados alterados com sucesso!")
    else:
        print(disco_resp)


if __name__ == '__main__':
    repor_estoque('', 9)
