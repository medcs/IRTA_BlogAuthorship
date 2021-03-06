import os
import re
import codecs
from string import punctuation
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
from nltk.corpus import stopwords

# parser = ET.XMLParser(encoding="utf-8")
parser = etree.XMLParser(recover=True)


def from_xml_to_plain_text(lower_case= False, remove_punctuation=False, remove_stopwors=False):
    source_dir = os.getcwd() + "/data/blogs/top90-100/"
    dest_dir = os.getcwd() + "/data/plainblogs/"
    if not os.path.exists(dest_dir):
        print("Create directory: " + dest_dir)
        os.makedirs(dest_dir)

    all_files = os.listdir(source_dir)
    for i, filename in enumerate(all_files):

        new_filename = filename.replace(".xml", ".txt")

        if not os.path.exists(dest_dir + new_filename):
            file_reader = codecs.open(source_dir + filename, 'r', encoding='utf-8', errors='ignore')
            # file_reader = open(source_dir + filename, 'r', encoding="utf8")
            content = file_reader.read()
            file_reader.close()

            # content = content.replace("&", "&amp;").replace("<3","&lt;3").replace("<3","&lt;3")
            root = etree.fromstring(content, parser=parser)  # ET.fromstring(content)

            # aggregate posts
            posts = ""
            for post in root.iter('post'):
                clean_post = post.text.strip()

                if lower_case:
                    clean_post = clean_post.lower()

                if remove_punctuation:
                    translation = str.maketrans("", "", punctuation)
                    clean_post = clean_post.translate(translation)

                if remove_stopwors:
                    stop_words = set(stopwords.words('english'))
                    clean_post = ' '.join([word for word in clean_post.split() if word not in stop_words])

                posts += clean_post + "\n"

            # remove last \n
            posts = posts[:-1]
            print(posts)

            # save content
            file_writer = open(dest_dir + new_filename, "a", encoding="utf8")
            file_writer.write(posts)
            file_writer.close()


def load_corpus(input_dir):
    from os import listdir
    from os.path import isfile, join

    trainfiles = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

    trainset = []
    for f in trainfiles:

        label = f
        df = pd.read_csv(input_dir + "/" + f, sep='\n', header=None,error_bad_lines=False)

        for row in df.iterrows():
            text = row[1][0]
            if type(text) is str:
                trainset.append({"label": label, "text": text})

    return trainset
