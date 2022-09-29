import requests
import xml.etree.ElementTree as ET

cellar = "http://publications.europa.eu/resource/cellar/fe93672d-fd84-414b-82ef-68da9cb805e3.0003.04/DOC_1"
celex = "http://publications.europa.eu/resource/celex/12012E.ENG.print"
oj = "http://publications.europa.eu/resource/oj/JOC_2012_326_R.ENG.fmx4.C_2012326EN.01000101.xml"
headers = {"Accept": "application/xml;notice=object",
           "Accept-Language": "eng"}
response = requests.get(celex, headers=headers)
response.raise_for_status()
data = response.text
root = ET.fromstring(data)

# for child in root:
#     for gchild in child:
#         print(gchild.tag, gchild.attrib)

with open("response.txt", "w") as file:
    file.write(data)

print(data)
