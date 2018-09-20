import re


def find_pattern(file_content):
    pattern = re.compile(r'http://www.rad.cvm.gov.br.+?NumeroSequencialDocumento=\d+')
    return pattern.findall(file_content)


def open_file(file_path):
    file = open(file_path, "r")
    file_content = file.read()
    return file_content.replace("\n", " ").replace("\r", " ")


if __name__ == '__main__':
    file_content = open_file("files/example.txt")
    patterns = find_pattern(file_content)

    print('\n'.join(patterns))
