import zipfile
import os
import slugify


def extract_zip(zip_file_path, target_path):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(target_path)
    zip_ref.close()


def unzip_internal_file(target_path):
    compressed_files = list(filter(lambda x: not 'xml' in x, os.listdir(target_path)))

    internal_path = target_path + '/internal'
    os.makedirs(internal_path)

    for file in compressed_files:
        extract_zip(target_path + '/' + file, internal_path)


def process_zip_file(number):
    target_path = 'extracted/{}'.format(number)

    if not os.path.exists(target_path):
        os.makedirs(target_path)
        extract_zip('downloaded/{}.zip'.format(number), target_path)
        unzip_internal_file(target_path)


if __name__ == '__main__':
    process_zip_file(72683)
