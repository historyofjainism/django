import xml.etree.ElementTree as ET
from pathlib import Path
import os 
from django.template.loader import render_to_string

BASE_DIR = Path(__file__).resolve().parent

def get_summary( article_name ):
    content_path = os.path.join(BASE_DIR, "content/article/" + article_name + ".html")
    content_xml = render_to_string(content_path)
    print(content_xml)
    content_et = ET.fromstring(content_xml)
    title = content_et.find("./article/header/div[@class='title']").text
    subtitle = content_et.find("./article/header/div[@class='subtitle']").text
    description = content_et.find("./article/header/div[@class='description']").text
    coverimg = content_et.find("./article/header/img[@class='coverimg']").get('src')
    return title, subtitle, description, coverimg