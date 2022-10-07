import requests
import zipfile


class Extractor:

    def __init__(self, celex_number):
        self.celex_number = celex_number
        self.uri = f"http://publications.europa.eu/resource/celex/{celex_number}"
        self.headers = {"Accept": "application/zip;mtype=fmx4",
                        "Accept-Language": "eng"}

    def get_zip(self):
        response = requests.get(self.uri, headers=self.headers)
        response.raise_for_status()

        with open("files/response.zip", mode="wb") as file:
            file.write(response.content)

        with zipfile.ZipFile("files/response.zip") as file:
            namelist = file.namelist()
            for name in namelist:
                if not name.endswith('doc.xml'):
                    file.extract(name, path="files/xml")
