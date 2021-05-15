from django.http import HttpResponse
from django.shortcuts import render

import xml.etree.ElementTree as ET
from pathlib import Path
import os 
BASE_DIR = Path(__file__).resolve().parent

def timeline(request, timeline_name):
    xmlfile = os.path.join(BASE_DIR,"content/timeline/" + timeline_name + ".xml")
    print(xmlfile)

    tree = ET.parse(xmlfile)
    root = tree.getroot()
    items = []
    timeline_obj = [ ]
    timeline = root.find('timeline')
    for item in timeline.findall('event'):
        eventjson = { }
        for child in item:
            eventjson[child.tag] = child.text
        timeline_obj.append(
            {
                'year' : eventjson['year'],
                'title' : eventjson['title'], 
                'description' : eventjson['description'][:300], 
                'link' : eventjson['link'],
                'type' : ( eventjson['type'] if 'type' in eventjson.keys() else 'default')
            })

    return render(
        request,
        'timeline.html', 
        {
            'timeline' : timeline_obj, 
            'title' : root.find('title').text,
            'coverimg' : "/static/images/timeline/" + root.find('cover_img').text,
            'samvat' : root.find('samvat').text
        } )

