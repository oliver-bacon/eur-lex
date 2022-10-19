import requests
import zipfile


class Extractor:
    def __init__(self, celex_number, language="eng"):
        self.celex_number = celex_number
        self.uri = f"http://publications.europa.eu/resource/celex/{celex_number}"
        self.headers = {
            "Accept": "application/zip;mtype=fmx4",
            # [aju] It's a minor thing, but you could make the language a parameter
            # [aju] of the class, so that you can easily switch between languages.
            # [aju] You can then set the default to "eng" so that users only have
            # [aju] to specify the language if they want another language than English.
            "Accept-Language": language,
        }

    def get_zip(self):
        response = requests.get(self.uri, headers=self.headers)
        # [aju] If you raise for status, you could add some error handling
        response.raise_for_status()

        # [aju] See my commend in main.py
        with open("files/response.zip", mode="wb") as file:
            file.write(response.content)

        # [aju] If you look at the lexparancy implementation, you can find a nice
        # [aju] use of a dictionary with the filenames as keys and ET.Elements as values.
        # [aju] This dictionary is then easy to pass around.
        with zipfile.ZipFile("files/response.zip") as file:
            namelist = file.namelist()
            for name in namelist:
                if not name.endswith("doc.xml"):
                    file.extract(name, path="files/xml")
