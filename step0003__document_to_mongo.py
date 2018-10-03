import os
from xml.etree.ElementTree import fromstring
from xmljson import parker as bf
import pymongo
import slugify


def read_file_as_json(file_path, field_name):
    print(file_path)
    file_open = open(file_path, "r")
    content = file_open.read()

    data = bf.data(fromstring(content))
    data['key_name'] = field_name

    return {slugify.slugify(field_name.replace('.xml', '')): data}


def concat_two_dicts_into_one(roots_json, internal_json):
    result = {}
    for d in roots_json:
        result.update(d)

    for d in internal_json:
        result.update(d)

    return result


def get_balanco_as_json(document_id):
    target_path = 'extracted/{}'.format(document_id)

    xml_root = filter(lambda x: 'xml' in x, os.listdir(target_path))
    internal_files = ['InfoFinaDFin.xml', 'PeriodoDemonstracaoFinanceira.xml']

    roots_json = list(map(lambda x: read_file_as_json(target_path + '/' + x, x), xml_root))
    internal_json = list(map(lambda x: read_file_as_json(target_path + '/internal/' + x, x), internal_files))

    concat = concat_two_dicts_into_one(roots_json, internal_json)
    concat['_id'] = document_id

    return concat


def join_period_with_valor(periodos, patr):
    the_dict = {}

    for period in periodos:
        the_dict[period['DataFimPeriodo'][:10]] = patr['ValorConta' + str(period['NumeroIdentificacaoPeriodo'])]

    return {patr['DescricaoConta1']: the_dict}


def extract_balance(id_from_bovespa):
    balanco_document = get_balanco_as_json(id_from_bovespa)

    periodos = balanco_document['periododemonstracaofinanceira']['PeriodoDemonstracaoFinanceira']
    info_financeiras = balanco_document['infofinadfin']['InfoFinaDFin']

    balanco_json = list(map(lambda x: join_period_with_valor(periodos, x), info_financeiras))

    #
    # recursivamente, tenho que tirar os . das chaves aqui
    #

    return {
        '_id': balanco_document['formulariocadastral']['CompanhiaAberta']['CodigoCvm'],
        'codigo_cvm': balanco_document['formulariocadastral']['CompanhiaAberta']['CodigoCvm'],
        'nome': balanco_document['formulariocadastral']['CompanhiaAberta']['NomeRazaoSocialCompanhiaAberta'].strip(),
        'balanco': balanco_json
    }


if __name__ == '__main__':
    balance = extract_balance(72683)
    print('balanco feito')
    # pegar balanco do mongo.
    # fazer join com o balanco extraido
    # persistir again no mongo

    mongoclient = pymongo.MongoClient("mongodb://user:passwd@localhost:27017/")
    mongodatabase = mongoclient["balancos"]
    collection = mongodatabase["balancos"]
    print('colecao de boas')
    one = collection.insert_one(balance)
    print('inserido')

    print(one)
