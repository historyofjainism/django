from django.http import HttpResponse
from django.shortcuts import render

import content

import xml.etree.ElementTree as ET
from pathlib import Path
import os 

from django.template.loader import render_to_string



BASE_DIR = Path(__file__).resolve().parent
EVENT_IMG_BASE_URL = "/static/images/timeline/"
COVER_IMG_BASE_URL = "/static/images/timeline/"
PROD_WEBSITE = "https://history-of-jainism.web.app"

EVENT_LINK_TEXT = { 'en' : "Read More", 'hi' : "और पढ़ें"}

def timeline(request, lang, timeline_name):
    xmlfile = os.path.join(BASE_DIR, "content/timeline/" + timeline_name + ".xml")
    root = ET.parse(xmlfile).getroot()

    timeline = root.find('timeline')
    timeline_obj = [ ]

    for t_event in timeline.findall('event'):
        e_title = t_event.find('title')
        e_desc = t_event.find('description')
        e_year = t_event.find('year')
        e_image = t_event.find('image')
        e_link = t_event.find('link')
        e_type = t_event.find('type')
        timeline_obj.append(
            {
                'title' : ( e_title.find(lang).text if (e_title.find(lang) is not None) else e_title.text ), 
                'description' : ( e_desc.find(lang).text[:300] if ( e_desc.find(lang) is not None) else e_desc.text), 
                'year' : e_year.text,
                'image' : ( EVENT_IMG_BASE_URL + e_image.text if (e_image is not None) else None ),
                'link' : ( e_link.text if (e_link is not None) else None ),
                'type' : ( e_type.text if (e_type is not None) else 'default')
            })

    return render(
        request,
        'timeline.html', 
        {
            'timeline' : timeline_obj, 
            'title' : root.find('title').find(lang).text,
            'description' : root.find('description').find(lang).text,
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : PROD_WEBSITE + COVER_IMG_BASE_URL + root.find('cover_img').text,
            'coverimg' : COVER_IMG_BASE_URL + root.find('cover_img').text,
            'samvat' : root.find('samvat').find(lang).text,
            'event_link_text' : EVENT_LINK_TEXT[lang],
            'lang' : lang,
            'lang_en_url' : '/timeline/en/' + timeline_name,
            'lang_hi_url' : '/timeline/hi/' + timeline_name
        } )

def webstory(request, lang, webstory_name):
    return render(
        request,
        'webstory.html',
        {
            'title' : "गच्छ",
            'description' : "गच्छ, कुल, गण और शाखाएं का पारिभाषिक अर्थ",
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : PROD_WEBSITE + '/static/images/gaccha.jpg',
            'coverimg' : '/static/images/gaccha.jpg',
        } ) 

def article(request, lang, article_name):
    title, subtitle, description, coverimg = content.get_summary( article_name )
    return render(
        request,
        'article.html',
        {
            'title' : title,
            'subtitle' : subtitle,
            'description' : description,
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : PROD_WEBSITE + coverimg,
            'article_content' : article_name + ".html",
        } ) 

def home( request ):
    return render(
        request,
        'index.html')


