import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def listar_discos(nome, artista, ano_lancamento, estilo):
    disco = Disco()
    disco_resp = disco.listar_discos(nome, artista, ano_lancamento, estilo)

    print(disco_resp)


if __name__ == '__main__':
    listar_discos(None, 'Charlie Brown Jr', None, None)
