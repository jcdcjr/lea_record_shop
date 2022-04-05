import boto3
from entidades.Cliente import Cliente

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def atualizar(documento, nome_completo, data_nascimento, email, telefone):
    cliente = Cliente(documento)
    cliente_resp = cliente.atualizar(nome_completo, data_nascimento, email, telefone, dynamodb)

    if not cliente_resp.__contains__('Erro:'):
        print("Dados alterados com sucesso!")
    else:
        print(cliente_resp)


if __name__ == '__main__':
    atualizar("11122233300", 'Jose Carlos de Campos Junior', '1986-01-23', 'jcdcjr@gmail.com', '11999990000')
