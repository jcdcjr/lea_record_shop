import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def realizar_baixa_estoque(disco_id, quantidade):
    disco = Disco()
    disco_resp = disco.realizar_baixa_estoque(disco_id, quantidade, dynamodb)

    if not disco_resp.__contains__('Erro:'):
        print("Baixa realizada com sucesso!")
    else:
        print(disco_resp)


if __name__ == '__main__':
    realizar_baixa_estoque('976a94e1-b493-11ec-97a5-085bd6526d3f', 2)
