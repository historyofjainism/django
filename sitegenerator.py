import requests
import views
import shutil
import os

HOST='http://127.0.0.1:8000'
DEPLOY_BASE='/Volumes/GoogleDrive-101816541391522989781/My Drive/firebase/build'
DIR_STRUCT = [
    DEPLOY_BASE + '/binder/hi',
    DEPLOY_BASE + '/binder/en',
    DEPLOY_BASE + '/binder/gu',
    DEPLOY_BASE + '/blog/en',
    DEPLOY_BASE + '/blog/hi',
    DEPLOY_BASE + '/ampstory',
]
FOLDERS = [
    '/Volumes/GoogleDrive-101816541391522989781/My Drive/django/deploy/static',
]
URLS = [
    ( '/index.html', '/' ),
]

def main():
    print("Cleaning up old directory: ", DEPLOY_BASE)
    shutil.rmtree(DEPLOY_BASE)
    print("Creating folders: ")
    for dir in DIR_STRUCT:
        print(dir)
        os.makedirs(dir)
    print("Copying folder: ", FOLDERS[0] )
    shutil.copytree(FOLDERS[0], DEPLOY_BASE + "/static")
    print("Begin Site Generation")
    content_list = views.home( None, generate_site=True )
    for binder in content_list['data']['binderCollection']['items']:
        URLS.append( 
            ( "/binder/" + binder['language'] + "/" + binder['name'] ,
              "/binder/" + binder['language'] + "/" + binder['name'] ) )
    for blog in content_list['data']['blogCollection']['items']:
        URLS.append( 
            ( "/blog/" + blog['language'] + "/" + blog['name'] ,
              "/blog/" + blog['language'] + "/" + blog['name'] ) )
    for ampstory in content_list['data']['ampStoryCollection']['items']:
        URLS.append( 
            ( "/ampstory/" + ampstory['name'] ,
              "/ampstory/" + ampstory['name'] ) )

    print("URL to generate site: ")
    for dest_path, src_path in URLS:
        url = HOST + src_path
        file_name = DEPLOY_BASE + dest_path
        print(url, file_name)
        r = requests.get(url, allow_redirects=True)
        file_d = open(file_name, 'wb')
        file_d.write(r.content)
        file_d.close()


if __name__ == '__main__':
    main()
