# [aju] If you're using third-party libraries, it's advisable to use a
# [aju] virtual environment and a requirements.txt file. This way, you can
# [aju] easily share your project with others and they can easily install
# [aju] all the dependencies.
# [aju] Here's some resouces on that topic: https://realpython.com/python-virtual-environments-a-primer/

# from lxml import etree as ET
import xml.etree.ElementTree as ET
from unicodedata import normalize


class Formex:
    def __init__(self, xml_filename):
        self.xml_filename = f"files/xml/{xml_filename}"
        self.tree = ET.parse(self.xml_filename)
        self.root = self.tree.getroot()

        # [aju] This is the wrong xpath.
        self.division = self.root.findall(
            "ENACTING.TERMS/DIVISION/ARTICLE/*[@IDENTIFIER]/ALINEA"
        )

        self.dict = {
            # [aju] This is the wrong xpath for the title.
            # [aju] The correct one would be `TITLE/TI` and then take the entire text.
            "Title": self.root.findall("TITLE/TI/P/HT")[0].text,
            "chapters": self.add_chapters(),
        }

        # print(self.root.findall("ENACTING.TERMS/DIVISION/TITLE/TI/P")[0].text)
        # print(self.chapters[2]["ch_num"])

    # [aju] If you write methods, it helps understandability if you add docstrings.
    # [aju] This is a resource on docstrings:
    # [aju] https://realpython.com/documenting-python-code/#documenting-your-python-code-base-using-docstrings
    def add_chapters(self):

        chapters_xml = self.root.findall("ENACTING.TERMS/DIVISION")
        chapters = []

        # [aju] I think this approach is a bit too complicated and error-prone.
        # [aju] Rather than using indices to refer to DIVISION or ARTICLE,
        # [aju] it would be easier to pass the entire DIVISION element around.
        # [aju] Coarsly, this would mean, look for all DIVISION, then pass the
        # [aju] DIVISION element to the add_articles function to extract all
        # [aju] articles. Then pass the ARTICLE element to the add_paragraphs.
        # [aju] You can actually use an XPath to get the DIVISION element, not only
        # [aju] on the root element.
        #
        # [aju] You approach is probably also the reason that your extraction is flawed.
        # [aju] If you loko at you dictionary at `chapters[0].articles[1].paragraphs[0]`,
        # [aju] you will see that the paragraph is actually the first paragraph of the
        # [aju] actually belong to 'Article 3' rather than 'Article 2'.
        for ch in range(1, len(chapters_xml) + 1):
            chapters.append(
                {
                    "ch_num": normalize(
                        "NFKC",
                        self.root.find(
                            f"ENACTING.TERMS/DIVISION[{ch}]/TITLE/TI/P"
                        ).text,
                    ),
                    "articles": self.add_articles(ch),
                }
            )

        return chapters

    def add_articles(self, ch_num):

        articles = []
        for ar in range(
            1, len(self.root.findall(f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE")) + 1
        ):
            articles.append(
                {
                    "ar_num": normalize(
                        "NFKC",
                        self.root.find(
                            f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar}]/TI.ART"
                        ).text,
                    ),
                    "ar_name": self.root.find(
                        f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar}]/STI.ART/P"
                    ).text,
                    "paragraphs": self.add_paragraphs(ar, ch_num),
                }
            )

        return articles

    def add_paragraphs(self, ch_num, ar_num):

        paragraphs = []
        for pa in range(
            1,
            len(
                self.root.findall(
                    f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG"
                )
            )
            + 1,
        ):

            p_num = self.root.find(
                f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG[{pa}]/NO.PARAG"
            )
            p_text = self.root.find(
                f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG[{pa}]/ALINEA"
            )
            if p_num.text is None:
                p_num = ""
            else:
                p_num = p_num.text
            if p_text.text is None:
                p_text = self.root.find(
                    f"ENACTING.TERMS/DIVISION[{ch_num}]/ARTICLE[{ar_num}]/PARAG[{pa}]/ALINEA/P"
                ).text
            else:
                p_text = p_text.text

            paragraphs.append({"p_num": p_num, "p_text": normalize("NFKC", p_text)})

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
