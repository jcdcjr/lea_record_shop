import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def obter_dados_disco(disco_id):
    disco = Disco()
    disco_resp = disco.obter_por_id(disco_id, dynamodb)

    print(disco_resp)


if __name__ == '__main__':
    obter_dados_disco('')