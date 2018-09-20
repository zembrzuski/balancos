import zipfile

def process_zip_file(number = 76884):
    # create directory
    # unzip file
    # read file that is not xml
    # unzip ip
    # create some list
    print("oi")



zip_ref = zipfile.ZipFile('downloaded/{}.zip'.format(number), 'r')
zip_ref.extractall('extracted')
zip_ref.close()
