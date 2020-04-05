'''
__author__: Fangbo Tao
__description__: Extract Zettels with meta information from evernote export.
__latest_updates__: 11/07/2019
'''
import argparse
import xml.etree.ElementTree as ET 
from bs4 import BeautifulSoup as BS
import re

def match_zettel_id(text):
    pattern = re.compile("^Z[0-9]+[A-Z]$")
    return pattern.match(text)



class Zettel:

    def __init__(self, xml_obj):
        self.xml_obj = xml_obj
        self.title = ""
        self.id = ""
        self.ever_url = "" # url used to refer an evernote note
        self.content = ""
        self.tags = set()
        self.related_zettels = set()
        self.related_zettel_ids = set()
        # detailed info
        self.todo = False
        self.parent_zettel = None
        self.parent_id = None
        self.children_zettels = []
        self.references = set() #set of strings


    def parse_content(self, content_xml):
        tree = ET.fromstring(content_xml.text)
        soup = BS(content_xml.text, features="html.parser")

        for link in soup.findAll('a'):
            if link.text.startswith('Z'):
                ref_id = link.text.split(' ')[0]
                self.related_zettel_ids.add(ref_id)

        if '@TODO' in content_xml.text:
            self.todo = True

        # find parent
        first_div = soup.findAll('div')[0]
        p_id = first_div.text.split(' ')[0]
        if match_zettel_id(p_id):
            self.parent_id = p_id


        # print(first_div.text)
            # if item.text is not None:
            #     print(item.text)
            #     soup = BS(item.text)
            #     print(soup)
            #     for link in soup.findAll('a'):
            #         print(link.get('href'))


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
                    # self.parse_content(zet, child)
                    zet.parse_content(child)
                elif child.tag == 'tag':
                    t = self.tags[child.text] if child.text in self.tags else Tag(child.text)
                    self.tags[child.text] = t
                    zet.tags.add(t)
                    t.zettels.add(zet)

            self.zettels[zet.id] = zet

        # after parsing all text, link the content together
        for zet in self.zettels.values():
            for related_zet_id in zet.related_zettel_ids:
                if related_zet_id in self.zettels:
                    zet.related_zettels.add(self.zettels[related_zet_id])
            # parse parent
            if zet.parent_id is not None:
                p_zettel = self.zettels[zet.parent_id]
                p_zettel.children_zettels.append(zet)
                zet.parent_zettel = p_zettel


    def output_basic(self):
        print('Number of zettels: %d' % len(self.zettels))
        print('Number of unfinished zettels: %d' % len([z for z in self.zettels.values() if z.todo == True]))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='extractor.py')
    parser.add_argument('-f', required=True, \
            help='Zettelkasten file for processing')
    args = parser.parse_args()

    zks = Zettelkasten(args.f)
    zks.extract_zettels()

    zks.output_basic()

    while True:
        command = input("command (tag | todo | zet | count) : ")

        if command == 'tag':
            tag = input("tag: ")  # Python 2
            if tag not in zks.tags:
                continue

            t = zks.tags[tag]
            for zet in t.zettels:
                print(zet.title)
                print(zet.tags)
            # print(zet.related_zettels)

        elif command == 'todo':
            for zet in zks.zettels.values():
                if zet.todo == True:
                    print(zet.title)

        elif command == 'zet':
            zet_id = input("zettel id: ")  # Python 2
            if zet_id not in zks.zettels:
                continue

            zet = zks.zettels[zet_id]
            print('Zet title: %s' % zet.title)
            print('Zet tags: %s' % ' | '.join([z.text for z in zet.tags]))
            print('Zet children: %s' % ' \n '.join([z.title for z in zet.children_zettels]))

        # elif command == 'count':



        print('\n\n')
