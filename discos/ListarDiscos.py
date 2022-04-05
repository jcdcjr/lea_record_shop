import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def listar_discos(nome, artista, ano_lancamento, estilo):
    disco = Disco()
    disco_resp = disco.listar_discos(nome, artista, ano_lancamento, estilo, dynamodb)

    print(disco_resp)


if __name__ == '__main__':
    # listar_discos(None, None, None, None)
    # listar_discos(None, 'Metallica', None, None)
    # listar_discos(None, None, '1991', None)
    # listar_discos(None, 'Gus', None, None)
    listar_discos('B', None, None, 'R')
