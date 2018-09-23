import requests
import os.path


def download(number):
    print(number)
    url = "http://www.rad.cvm.gov.br/enetconsulta/frmDownloadDocumento.aspx?CodigoInstituicao=2&NumeroSequencialDocumento={}".format(number)
    r = requests.get(url)
    open('downloaded/{}.zip'.format(number), 'wb').write(r.content)


for x in reversed(range(12917, 77225)):
    already_downloaded = os.path.isfile('downloaded/{}.zip'.format(x))
    if already_downloaded:
        print("skipped {}".format(x))
    else:
        print("downloading {}".format(x))
        download(x)
