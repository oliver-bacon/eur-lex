from extraction import Extractor
from os import listdir
from formex import Formex
import pprint

celex_number = "32008R0593"

extc = Extractor(celex_number)
extc.get_zip()

filename = input(f"Files:\n{listdir('./files/xml')}\nPlease choose a file:\n")
frmx = Formex(filename)

with open("files/dict.txt", "w") as file:
    file.write(pprint.pformat(frmx.to_dict()))

# print(frmx.to_dict()["chapters"][2]["articles"][1]["paragraphs"][0]["p_text"])