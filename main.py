from extraction import Extractor
from os import listdir
from formex import Formex
import pprint

celex_number = "32008R0593"

extc = Extractor(celex_number)

# [aju] You could return the entire ZIP file, then you would not need to write
# [aju] it to disk. Writing to disk is comparatively slow.
extc.get_zip()

# [aju] This is a nice touch! But you actually also need the .doc.xml file,
# [aju] because it contains important information about the structure of the zip file.
filename = input(f"Files:\n{listdir('./files/xml')}\nPlease choose a file:\n")

# [aju] Here you could pass the ZIP file object rather than loading from disk
frmx = Formex(filename)

# [aju] If you write the Python dict to disk, you need to use a .py file.
# [aju] It would be better though to use a JSON file, because it is more
# [aju] usable in other systems.
# [aju] You could also add the functionality to the Fromex class.
with open("files/dict.json", "w") as file:
    file.write(pprint.pformat(frmx.to_dict()))

# print(frmx.to_dict()["chapters"][2]["articles"][1]["paragraphs"][0]["p_text"])
