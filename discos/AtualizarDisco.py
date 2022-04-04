import boto3
from entidades.Disco import Disco

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def atualizar_dados_disco(disco_Id, nome, artista, ano_lancamento, estilo):
    disco = Disco()
    disco_resp = disco.atualizar_dados_disco(disco_Id, nome,artista, ano_lancamento, estilo, dynamodb)

    if not disco_resp.__contains__('Erro:'):
        print("Dados alterados com sucesso!")
    else:
        print(disco_resp)


if __name__ == '__main__':
    atualizar_dados_disco('', 'Preco Curto, Prazo Longo', 'Charlie Brown Jr', 1997, 'Rock')
