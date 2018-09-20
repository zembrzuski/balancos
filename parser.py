import re


def find_pattern(file_content):
    pattern = re.compile(r'http://www.rad.cvm.gov.br.+?NumeroSequencialDocumento=\d+')
    return pattern.findall(file_content)


def open_file(file_path):
    file = open(file_path, "r")
    file_content = file.read()
    return file_content.replace("\n", " ").replace("\r", " ")


def open_file_and_extract_refs():
    file_content = open_file("files/example.txt")
    patterns = find_pattern(file_content)

    print('\n'.join(patterns))
