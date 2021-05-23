import requests
HOST='http://127.0.0.1:8000/'
TIMELINE_BASE = HOST + 'timeline/'
LANG = [ 'en/', 'hi/' ]
TIMELINES = [ 
    'ahojinshashan'
]

DEPLOY_BASE='deploy/'
DEPLOY_TIMELINE_BASE = DEPLOY_BASE + 'timeline/'

def main():
    for timeline in TIMELINES:
        for lang in LANG:
            timeline_url = TIMELINE_BASE + lang + timeline
            print(timeline_url)
            r = requests.get(timeline_url, allow_redirects=True)
            timeline_file_name = DEPLOY_TIMELINE_BASE + lang + timeline
            print(timeline_file_name)
            timeline_file = open(timeline_file_name, 'wb')
            timeline_file.write(r.content)
            timeline_file.close()


if __name__ == '__main__':
    main()
