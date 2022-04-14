"""
Performs Server Side Rendering for different
view types. The supported view types are as follows
ampstory, binder, storyblok, book.

There are also other helper methods which facilitates
in generating the view.
"""
import os
import json
import requests

from django.shortcuts import render
from django.conf import settings

CMS_CONTENTFUL = 1
CMS_STORYBLOK = 2

PROD_WEBSITE = "https://historyofjainism.com"

AMP = '⚡'

def context_processor( request ):
    """
    Defines a Context Processor
    which adds APP_ENVRIONMENT and prod_url
    to the data context.
    """
    data = { }
    data['APP_ENVIRONMENT'] = os.environ['APP_ENVIRONMENT']
    data['prod_url'] = PROD_WEBSITE + request.path
    return data

def ampstory(request, name):
    """
    Queries content from Contentful
    and renders it in AMPStory format.

    @param request - HTTP Request
    @param name - Slug name of the content
    """
    query = """
        query($name : String) {
            ampStoryCollection(limit: 1, where: {name: $name}) {
                items {
                    sys {
                        id
                    }
                    title,
                    subtitle
                    description,
                    story {
                        json
                        links {
                            assets {
                                block {
                                    url
                                    sys {
                                        id
                                    }
                                }
                            }
                        }
                    },
                    cover,
                    template
                }
            }
        }
    """
    res_json = get_content_as_json(query, {"name": name})
    context = res_json['data']['ampStoryCollection']['items'][0]
    context['AMP'] = AMP
    context['theme'] = "theme/black.css"

    image_blocks = context['story']['links']['assets']['block']
    image_urls = {}
    for image_block in image_blocks:
        image_urls[image_block['sys']['id']] = image_block['url']

    pages = []
    page = []
    for element in context['story']['json']['content']:
        if element['nodeType'] == 'hr':
            pages.append(page)
            page = []
        elif element['nodeType'] == 'paragraph':
            page.append({
                "type": "paragraph",
                "value": element['content'][0]['value']
            })
        elif element['nodeType'] == 'embedded-asset-block':
            page.append({
                "type": "image",
                "src": image_urls[element['data']['target']['sys']['id']]
            })
        elif element['nodeType'] == 'heading-3':
            page.append({
                "type": "heading-3",
                "value": element['content'][0]['value']
            })
        elif element['nodeType'] == 'heading-2':
            page.append({
                "type": "heading-2",
                "value": element['content'][0]['value']
            })
        elif element['nodeType'] == 'heading-1':
            page.append({
                "type": "heading-1",
                "value": element['content'][0]['value']
            })
        elif element['nodeType'] == 'unordered-list':
            page.append({
                "type": "unordered-list",
                "list_items": [
                    listitem['content'][0]['content'][0]['value']
                    for listitem in element['content']
                ]
            })
        elif element['nodeType'] == 'ordered-list':
            page.append({
                "type": "ordered-list",
                "list_items": [
                    listitem['content'][0]['content'][0]['value']
                    for listitem in element['content']
                ]
            })
    context['pages'] = pages
    return render(request, context['template'], context)

def binder(request, lang, name):
    """
    Queries content from Contentful in the language
    requested and renders it in Binder format.

    @param request - HTTP Request
    @param lang - Language of the Content
    @param name - Slug name of the content
    """
    query = """
       query($name: String, $lang: String) {
            binderCollection(limit:1, where: {name: $name, language: $lang}) {
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
    res_json = get_content_as_json(query, {"name": name, "lang": lang})
    binder_item_data = res_json['data']['binderCollection']['items'][0]
    return render(request, 'binder.html', {
        'lang': lang,
        'name': name,
        'binder': binder_item_data,
        'title': binder_item_data['title'],
        'subtitle': binder_item_data['subtitle'],
        'description': binder_item_data['subtitle'],
        'prod_url': PROD_WEBSITE + request.path,
        'linkpreview_img': binder_item_data['cover'][0]['url']
    })

def blog(request, lang, name, preview=False):
    """
    Queries content from Contentful in the language
    requested and renders it in Blog format.

    @param request - HTTP Request
    @param lang - Language of the Content
    @param name - Slug name of the content
    """
    query = """
        query($name: String, $lang: String, $preview: Boolean) {
            blogCollection(limit:1, preview: $preview, where: {name: $name, language: $lang}) {
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
    if not preview:
        res_json = get_content_as_json(query, {"name": name, "lang": lang})
    else:
        res_json = get_preview_content_as_json(query, {"name": name, "lang": lang, "preview": preview})
    blog_item_data = res_json['data']['blogCollection']['items'][0]
    return render(request, 'blog.html', {
        'lang': lang,
        'name': name,
        'blog': blog_item_data,
        'title': blog_item_data['title'],
        'subtitle': blog_item_data['subtitle'],
        'description': blog_item_data['subtitle'],
        'prod_url': PROD_WEBSITE + request.path,
        'linkpreview_img': blog_item_data['cover'][0]['url']
    })

def previewBlog(request, lang, name):
    return blog(request, lang, name, True)

def get_content_as_json(query, variables=None, cms=CMS_CONTENTFUL):
    """
    Makes an HTTP call to the CMS to fetch content as JSON

    @param query - A GraphQL Query
    @param variables - Variables required to render GraphQL Query
    @param cms - Content Management System from which content needs to be fetched
    """
    if cms == CMS_CONTENTFUL:
        headers = {
            "Authorization": f"Bearer {settings.CONTENTFUL_AUTHORIZATION_TOKEN}",
            "Content-Type": "application/json"
        }
        url = settings.CONTENTFUL_URL
    else:  # CMS==CMS_STORYBLOK
        headers = {
            "Token": settings.STORYBLOCK_AUTHORIZATION_TOKEN,
            "Version": "published" if os.environ['APP_ENVIRONMENT'] == "production" else "draft"
        }
        url = settings.STORYBLOK_URL
    response = requests.post(
        url,
        headers=headers,
        json={"query": query, "variables": variables}
    )
    return json.loads(response.text)

def get_preview_content_as_json(query, variables=None, cms=CMS_CONTENTFUL):
    """
    Makes an HTTP call to the CMS to fetch the Draft content as JSON
    """
    headers = {
        "Authorization": f"Bearer {settings.CONTENTFUL_AUTHORIZATION_TOKEN}",
        "Content-Type": "application/json"
    }
    url = settings.CONTENTFUL_URL
    response = requests.post(
        url,
        headers=headers,
        json={"query": query, "variables": variables}
    )
    return json.loads(response.text)

def appdynamic(request):
    """
    TODO: Needs better documentation
    """
    return render(request, 'menu-share.html')

def appkit(request):
    """
    Renders the content using AppKit

    @param request - HTTP Request
    """
    name = "tirthankarmahaveer1"
    query = """
        query($name : ID! ) {
            BookItem( id : $name ) {
                id,
                name,
                slug,
                full_slug,
                content {
                    title,
                    author,
                    subtitle,
                    description,
                    language,
                    cover {
                        filename
                    },
                    body
                }
            }
        }
    """
    res_json = get_content_as_json(
        query, {"name": "book/" + name}, CMS_STORYBLOK)
    print(res_json)
    # compatibility with contentful
    res_json['data']['BookItem']['content']['cover']['0'] = {
        'secure_url': res_json['data']['BookItem']['content']['cover']['filename']}
    return render(request, 'appkitdemo.html', res_json['data']['BookItem']['content'])

def home(request, generate_site=False):
    """
    Renders home page of History of Jainism

    @param request - HTTP Request
    @param generate_site
    """
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
            ampStoryCollection {
                items {
                    typename : __typename
                    name
                    title
                    subtitle
                    cover
                    updated
                }
            }
        }
    """
    res_json = get_content_as_json(query)
    print(res_json)
    if generate_site:
        return res_json
    print(res_json)
    all_items = res_json['data']['externalCollection']['items'] \
        + res_json['data']['binderCollection']['items'] \
        + res_json['data']['blogCollection']['items'] \
        + res_json['data']['ampStoryCollection']['items']
    print("sorted: ", all_items)
    content = {
        'title': "History of Jainism",
        'subtitle': "It's time Real Jain History be told!!",
        'description': "It's time Real Jain History be told!!",
        'prod_url': PROD_WEBSITE + request.path,
        'cards': sorted(all_items, key=lambda x: x['updated'], reverse=True)
        # 'linkpreview_img' : binder['cover'][0]['url']
    }
    return render(request, 'home.html', content)

def book(request, name):
    """
    Queries content from Storyblock and
    renders it in Blog format.

    @param request - HTTP Request
    @param name - Slug name for content
    """
    query = """
        query($name : ID! ) {
            BookItem( id : $name ) {
                id,
                name,
                slug,
                full_slug,
                content {
                    title,
                    author,
                    subtitle,
                    description,
                    language,
                    cover {
                        filename
                    },
                    body
                }
            }
        }
    """
    res_json = get_content_as_json(
        query, {"name": "book/" + name}, CMS_STORYBLOK)
    print(res_json)
    # compatibility with contentful
    res_json['data']['BookItem']['content']['cover']['0'] = {
        'secure_url': res_json['data']['BookItem']['content']['cover']['filename']}
    return render(request, 'book.html', res_json['data']['BookItem']['content'])
