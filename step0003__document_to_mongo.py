import os
from xml.etree.ElementTree import fromstring

from xmljson import badgerfish as bf


def read_file_as_json(file_path, field_name):
    print(file_path)
    file_open = open(file_path, "r")
    content = file_open.read()
    return {field_name: bf.data(fromstring(content))}


def concat_dicts(a, b):
    result = {}
    for d in a:
        result.update(d)

    for d in b:
        result.update(d)

    return result


def do_import(document_id):
    target_path = 'extracted/{}'.format(document_id)

    xml_internal = os.listdir(target_path + '/internal')
    xml_root = filter(lambda x: 'xml' in x, os.listdir(target_path))

    roots_json = list(map(lambda x: read_file_as_json(target_path + '/' + x, x), xml_root))
    internal_json = list(map(lambda x: read_file_as_json(target_path + '/internal/' + x, x), xml_internal))

    concat = concat_dicts(roots_json, internal_json)
    concat['doc_id'] = document_id

    print("po")


if __name__ == '__main__':
    do_import(76884)
