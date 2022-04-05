import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def cadastrar(nome, artista, ano_lancamento, estilo):
    disco = Disco()
    disco_resp = disco.cadastrar(nome, artista, ano_lancamento, estilo, dynamodb)

    if not disco_resp.__contains__('Erro:'):
        print("Disco cadastrado com sucesso!")
    else:
        print(disco_resp)


if __name__ == '__main__':
    cadastrar('Preco Curto Prazo Longo', 'Charlie Brown Jr', 1999, 'Rock Nacional')
    cadastrar('Greatest Songs', 'Bruno Mars', 2018, 'Pop')