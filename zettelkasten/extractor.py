'''
__author__: Fangbo Tao
__description__: Extract Zettels with meta information from evernote export.
__latest_updates__: 11/07/2019
'''
import argparse
import xml.etree.ElementTree as ET 
from bs4 import BeautifulSoup as BS

class Zettel:

    def __init__(self, xml_obj):
        self.xml_obj = xml_obj
        self.title = ""
        self.id = ""
        self.ever_url = "" # url used to refer an evernote note
        self.content = ""
        self.tags = set()
        self.references = set() #set of strings
        self.related_zettels = set()
        self.related_zettel_ids = set()

    def __repr__(self):
        return self.title


class Tag:

    def __init__(self, text):
        self.text = text
        self.zettels = set()
        # tag graph not supported for now
        self.ancestors = set()
        self.children = set()

    def __repr__(self):
        return '<tag> ' + self.text


class Zettelkasten:

    def __init__(self, archive_f):
        self.archive_f = archive_f
        self.tags = {}
        self.zettels = {}
        

    def extract_zettels(self):
        # Extract Zettels from archive file
        tree = ET.parse(self.archive_f)
        root = tree.getroot()

        for item in root.findall('./note'):
            zet = Zettel(item)

            for child in item:
                if child.tag == 'title':
                    zet.title = child.text
                    zet.id = zet.title.split(' ')[0]
                elif child.tag == 'content':
                    self.parse_content(zet, child)
                elif child.tag == 'tag':
                    t = self.tags[child.text] if child.text in self.tags else Tag(child.text)
                    self.tags[child.text] = t
                    zet.tags.add(t)
                    t.zettels.add(zet)

            self.zettels[zet.id] = zet

        for zet in self.zettels.values():
            for related_zet_id in zet.related_zettel_ids:
                if related_zet_id in self.zettels:
                    zet.related_zettels.add(self.zettels[related_zet_id])


    def parse_content(self, zet, content_xml):
        tree = ET.fromstring(content_xml.text)
        soup = BS(content_xml.text, features="html.parser")

        for link in soup.findAll('a'):
            if link.text.startswith('Z'):
                ref_id = link.text.split(' ')[0]
                zet.related_zettel_ids.add(ref_id)
        
        # for item in tree.findall('div'):
        #     if item.text is not None:
        #         print(item.text)
        #         soup = BS(item.text)
        #         print(soup)
        #         for link in soup.findAll('a'):
        #             print(link.get('href'))
        
        None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='extractor.py')
    parser.add_argument('-f', required=True, \
            help='Zettelkasten file for processing')
    args = parser.parse_args()

    zks = Zettelkasten(args.f)
    zks.extract_zettels()

    while True:
        tag = input("tag: ")  # Python 2
        if tag not in zks.tags:
            continue

        t = zks.tags[tag]
        for zet in t.zettels:
            print(zet.title)
            print(zet.tags)
            # print(zet.related_zettels)

