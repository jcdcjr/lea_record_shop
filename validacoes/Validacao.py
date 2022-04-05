from dateutil import parser
import re
import uuid


def validar_ano_lancamento(ano_lancamento):
    try:
        if len(ano_lancamento) != 4:
            return False
        res = bool(int(ano_lancamento))
    except ValueError:
        res = False
    return res


def validar_artista(artista):
    return len(artista) > 1


def validar_cliente(nome_completo, data_nascimento, email, telefone):
    if not nome_completo:
        return 'Erro: Nome completo é obrigatorio!'
    else:
        if not validar_nome_completo(nome_completo):
            return 'Erro: Nome completo invalido!'

    if not data_nascimento:
        return 'Erro: Data de nascimento é obrigatorio!'
    else:
        if not validar_data_nascimento(data_nascimento):
            return 'Erro: Data de nascimento invalida!'

    if not email:
        return 'Erro: E-mail é obrigatorio!'
    else:
        if not validar_email(email):
            return 'Erro: E-mail invalido!'

    if not telefone:
        return 'Erro: Telefone é obrigatorio!'
    else:
        if not validar_telefone(telefone):
            return 'Erro: Telefone invalido!'

    return None


def validar_data_nascimento(data_nascimento):
    try:
        res = bool(parser.parser(data_nascimento))
    except ValueError:
        res = False
    return res


def validar_data_hora_pedido(data_hora_pedido):
    try:
        res = bool(parser.parser(data_hora_pedido))
    except ValueError:
        res = False
    return res


def validar_disco(nome, artista, ano_lancamento, estilo):
    if not nome:
        return 'Erro: Nome do disco é obrigatório!'
    if not validar_nome_disco:
        return 'Erro: Nome do disco inválido!'

    if not artista:
        return 'Erro: Artista é obrigatório!'
    if not validar_artista:
        return 'Erro: Artista inválido!'

    if not ano_lancamento:
        return 'Erro: Ano de lançamento é obrigatório!'
    if not validar_ano_lancamento:
        return 'Erro: Ano de lançamento inválido!'

    if not estilo:
        return 'Erro: Nome do estilo é obrigatório!'
    if not validar_estilo:
        return 'Erro: Nome do estilo inválido!'

    return None


def validar_disco_id(disco_id):
    try:
        uuid.UUID(disco_id)
        return True
    except ValueError:
        return False


def validar_documento(documento):
    return len(documento) > 7


def validar_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    try:
        res = re.search(regex, email)
    except ValueError:
        res = False
    return res


def validar_estilo(estilo):
    return len(estilo) > 2


def validar_nome_completo(nome_completo):
    if len(nome_completo) < 5:
        return False
    return True


def validar_nome_disco(nome):
    return len(nome) > 1


def validar_quantidade(quantidade):
    try:
        if bool(int(quantidade)):
            return True
        return int(quantidade) > 0
    except ValueError:
        return False


def validar_pedido(documento, disco_id, quantidade):
    if not documento:
        return 'Erro: Documento é obrigatório!'

    if not validar_documento(documento):
        return 'Erro: Documento inválido!'

    if not disco_id:
        return 'Erro: Código do disco é obrigatório!'

    if not validar_disco_id(disco_id):
        return 'Erro: Código do disco inválido!'

    if not quantidade:
        return 'Erro: Quantidade é obrigatória!'

    if not validar_quantidade(quantidade):
        return 'Erro: Quantidade inválida!'

    return None


def validar_telefone(telefone):
    try:
        if len(telefone) < 10 & len(telefone) > 11:
            return False
        res = int(telefone)
    except ValueError:
        res = False
    return res
