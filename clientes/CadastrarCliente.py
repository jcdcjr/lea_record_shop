import boto3
from entidades.Cliente import Cliente

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def cadastrar(documento, nome_completo, data_nascimento, email, telefone):
    cliente = Cliente(documento)
    cliente_resp = cliente.cadastrar(nome_completo, data_nascimento, email, telefone, dynamodb)

    if not cliente_resp.__contains__('Erro:'):
        print("Cliente cadastrado com sucesso!")
    else:
        print(cliente_resp)


if __name__ == '__main__':
    cadastrar("11122233300", 'Jose Carlos de Campos Junior', '1986-01-23', 'jcdcjr@teste.com', '11999990000')
    cadastrar("11122244400", 'Eduardo Araujo', '2003-05-24', 'eduardo@teste.com', '11999991111')
    cadastrar("11122255500", 'Erika Rodrigues da Silva', '1987-10-26', 'erikasilva@teste.com', '11999992222')