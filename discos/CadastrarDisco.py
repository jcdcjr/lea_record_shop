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
    cadastrar("Black Album", "Metallica", 1991, "Rock")
    cadastrar("Preco Curto Prazo Longo", "Charlie Brown Jr", 1999, "Rock")
    cadastrar("Ten", "Pearl Jam", 1991, "Rock")
    cadastrar("Best of", "Bob Marley", 2007, "Reggae""")
    cadastrar("Nativus", "Natiruts", 1997, "Reggae")
    cadastrar("Tudo em Paz", "Jorge e Mateus", 2021, "Sertanejo")
    cadastrar("Buteco do Gusttavo Lima Vol 1", "Gusttavo Lima", 2015, "Sertanejo")
    cadastrar("Acusthico", "Thiaguinho", 2019, "Pagode")
    cadastrar("Sobrevivendo no Inferno", "Racionais Mc", 1997, "Rap")
    cadastrar("Greatest Songs", "Bruno Mars", 2018, "Pop")
