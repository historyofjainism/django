#
# Views
#  - home
#  - timeline[hindi/english]
#  - blog[hindi/english]
#  - binder[hindi/gujarati]
#  - ampstory[english/hindi]
#  - quiz[hindi]
#  - videos[english/hindi]
#  - course[hindi]

from django.http import HttpResponse
from django.shortcuts import render

import content

import xml.etree.ElementTree as ET
from pathlib import Path
import os 

from django.template.loader import render_to_string

import requests
import json

CMS_URL= "https://graphql.contentful.com/content/v1/spaces/skavkfrlakjq/environments/master"
CDN_URL="https://res.cloudinary.com/history-of-jainism/image/upload/v1634199762/"

BASE_DIR = Path(__file__).resolve().parent
EVENT_IMG_BASE_URL = "/static/images/timeline/"
COVER_IMG_BASE_URL = "/static/images/timeline/"
PROD_WEBSITE = "https://historyofjainism.com"

EVENT_LINK_TEXT = { 'en' : "Read More", 'hi' : "और पढ़ें"}

def timeline_old(request, lang, timeline_name):
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
    title, subtitle, description, coverimg = content.link_metadata( request.path )
    #title, subtitle, description, coverimg = content.get_summary( lang, article_name )
    return render(
        request,
        'article.html',
        {
            'title' : title,
            'subtitle' : subtitle,
            'description' : description,
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : PROD_WEBSITE + coverimg,
            'article_content' : lang + '/' + article_name + ".html",
        } ) 

def ampstory( request ):
    return render( request, 'gaccha.html')

def index( request ):
    return render(
        request,
        'index.html')

def timeline( request, lang, timeline_name ):
    title, subtitle, description, coverimg = content.link_metadata( request.path )
    print(request.path)
    return render(
        request,
        'timeline.html',
        {
            'lang' : lang,
            'title' : title,
            'subtitle' : subtitle,
            'description' : description,
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : PROD_WEBSITE + coverimg,
            'content' : "timeline/" + lang + "/" + timeline_name + ".html",
        } ) 

def library( request, lang, shelf_name ):
    return render( request, 'library.html', {
            'lang' : lang,
            'title' : 'Vikramaditya',
            'subtitle' : 'विक्रमादित्य के नाम पर विक्रम संवत २०७८(2021) चल रहा है।',
            'description' : 'विक्रमादित्य के नाम पर विक्रम संवत २०७८(2021) चल रहा है।',
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : PROD_WEBSITE + '/static/images/timeline/vikramaditya.jpg'
        } )

def binder( request, lang, name ):
    query = """
       query {
            binderCollection(limit:1, where: {name:\"""" + name + """\", language:\"""" + lang + """\"}) {
                items {
                    title     
                    subtitle
                    cover
                    description
                    clipsCollection {
                        items {
                            sys {
                                id
                            }
                            title
                            abstract
                            source {
                                    type
                                    title
                                    author
                                cover {
                                  url
                                }
                                serial
                            }
                            document {
                                url
                            }
                            pages
                            author
                        }
                    }
                }
            }
        }   
    """
    res_json = get_content_as_json(query)
    binder = res_json['data']['binderCollection']['items'][0]
    return render( request, 'binder.html', {
            'lang' : lang,
            'name' : name,
            'binder' : binder,
            'title' : binder['title'],
            'subtitle' : binder['subtitle'],
            'description' : binder['subtitle'],
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : binder['cover'][0]['url']
        } )

def blog( request, lang, name ):
    query = """
        query {
            blogCollection(limit:1, where: {name:\"""" + name + """\", language:\"""" + lang + """\"}) {
                items {
                    title
                    subtitle
                    cover
                    description
                    article
                    articleMore
                    translator
                    compiler
                    sourcesCollection {
                        items {
                            title
                            author
                        }
                    }
                }
            }
        }
    """
    res_json = get_content_as_json(query)
    blog = res_json['data']['blogCollection']['items'][0]
    return render( request, 'blog.html', {
            'lang' : lang,
            'name' : name,
            'blog' : blog,
            'title' : blog['title'],
            'subtitle' : blog['subtitle'],
            'description' : blog['subtitle'],
            'prod_url' : PROD_WEBSITE + request.path,
            'linkpreview_img' : blog['cover'][0]['url']
        } )

def get_content_as_json( query ):
    print(query)
    r = requests.post( CMS_URL, headers={
            "Authorization": "Bearer px87wXacTSetoV42SIP1YlO5Ace7MZMGAx9bMjDAJ3I",
            "Content-Type": "application/json"
        },
        json={"query": query}
    )

    return json.loads(r.text)


def home( request ):
    query = """
        query {
            externalCollection {
                items {
                    typename : __typename
                    title
                    subtitle
                    url
                    cover
                    type
                    updated
                }    
            }
            binderCollection {
                items {
                    typename : __typename
                    name
                    language
                    title
                    subtitle
                    cover
                    updated
                }
            }
            blogCollection {
                items {
                    typename : __typename
                    name
                    language
                    title
                    subtitle
                    cover
                    updated
                }
            }            
        }
    """
    res_json = get_content_as_json( query )
    print(res_json)
    all_items = res_json['data']['externalCollection']['items'] \
                + res_json['data']['binderCollection']['items'] \
                + res_json['data']['blogCollection']['items'] 
    print("sorted")
    return render( request, 'home.html', {
            'title' : "History of Jainism",
            'subtitle' : "It's time Real Jain History be told!!",
            'description' : "It's time Real Jain History be told!!",
            'prod_url' : PROD_WEBSITE + request.path,
            'cards' : sorted(all_items, key=lambda x:x['updated'], reverse=True)
            #'linkpreview_img' : binder['cover'][0]['url']
        } )

