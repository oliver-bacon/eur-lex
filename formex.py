# from lxml import etree as ET
import xml.etree.ElementTree as ET
from unicodedata import normalize


class Formex:

    def __init__(self, xml_filename):
        self.xml_filename = f"files/xml/{xml_filename}"
        self.tree = ET.parse(self.xml_filename)
        self.root = self.tree.getroot()
        self.division = self.root.findall("ENACTING.TERMS/DIVISION/ARTICLE/*[@IDENTIFIER]/ALINEA")

        self.dict = {
            "Title": self.root.findall("TITLE/TI/P/HT")[0].text,
            "chapters": self.add_chapters()
        }

        # print(self.root.findall("ENACTING.TERMS/DIVISION/TITLE/TI/P")[0].text)
        # print(self.chapters[2]["ch_num"])

    def add_chapters(self):

        chapters_xml = self.root.findall("ENACTING.TERMS/DIVISION")
        chapters = []
        for ch in range(1, len(chapters_xml) + 1):
            chapters.append({"ch_num": normalize('NFKC', self.root.find(f"ENACTING.TERMS/DIVISION[{ch}]/TITLE/TI/P").text),
                             "articles": self.add_articles(ch)})

        return chapters

    def add_articles(self, ch_num):

        articles = []
        for ar in range(1, len(self.root.findall(f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE")) + 1):
            articles.append({
                "ar_num": normalize('NFKC', self.root.find(f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar}]/TI.ART").text),
                "ar_name": self.root.find(f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar}]/STI.ART/P").text,
                "paragraphs": self.add_paragraphs(ar, ch_num)})

        return articles

    def add_paragraphs(self, ch_num, ar_num):

        paragraphs = []
        for pa in range(1, len(self.root.findall(f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG")) + 1):

            p_num = self.root.find(f'ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG[{pa}]/NO.PARAG')
            p_text = self.root.find(f'ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG[{pa}]/ALINEA')
            if p_num.text is None:
                p_num = ""
            else:
                p_num = p_num.text
            if p_text.text is None:
                p_text = self.root.find(f'ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG[{pa}]/ALINEA/P').text
            else:
                p_text = p_text.text

            paragraphs.append({
                "p_num": p_num,
                "p_text": normalize('NFKC', p_text)
            })

        return paragraphs

    def print_para(self):
        for para in self.division:
            print(para.text)

    def to_dict(self):
        return self.dict

    # self.dict = [
    #     {
    #         "Title": self.root.find("TITLE/TI/P/HT").text,
    #         "chapters": {
    #             "ch_num": self.root.findall("ENACTING.TERMS/DIVISION/TITLE/TI/P"),
    #             "articles": {
    #                 "ar_num": self.root.findall("ENACTING.TERMS/DIVISION/ARTICLE/TI.ART"),
    #                 "ar_name": self.root.findall("ENACTING.TERMS/DIVISION/ARTICLE/STI.ART/P"),
    #                 "paragraphs": {
    #                     "p_num": self.root.findall("ENACTING.TERMS/DIVISION/ARTICLE/PARAG/NO.PARAG"),
    #                     "p_text": self.root.findall("ENACTING.TERMS/DIVISION/ARTICLE/PARAG/ALINEA/P")
    #                 }
    #             }
    #         }
    #     }
    # ]
