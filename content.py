import xml.etree.ElementTree as ET
from pathlib import Path
import os 
from django.template.loader import render_to_string

BASE_DIR = Path(__file__).resolve().parent

def get_summary( lang, article_name ):
    content_path = os.path.join(BASE_DIR, "content/article/" + lang + '/' + article_name + ".html")
    content_xml = render_to_string(content_path)
    print(content_xml)
    content_et = ET.fromstring(content_xml)
    title = content_et.find("./article/header/div[@class='title']").text
    subtitle = content_et.find("./article/header/div[@class='subtitle']").text
    description = content_et.find("./article/header/div[@class='description']").text
    coverimg = content_et.find("./article/header/img[@class='coverimg']").get('src')
    return title, subtitle, description, coverimg

def link_metadata( content_path ):
    content_file = os.path.join(BASE_DIR, "content/" + content_path + ".html")
    content_xml = render_to_string(content_file)
    print(content_xml)
    content_et = ET.fromstring(content_xml)
    title = content_et.find("./header/h1").text
    subtitle = content_et.find("./header/h2").text
    description = content_et.find("./header/p").text
    coverimg = content_et.find("./header/img").get('src')
    return title, subtitle, description, coverimg