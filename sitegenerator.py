import requests
HOST='http://127.0.0.1:8000/'

PATHs = [
    'index.html',
    'timeline/hi/nirgrantha',
    'article/en/javadshah',
    'article/en/khemaderani',
    'article/hi/kangra',
    'article/hi/taksasila',
]

DEPLOY_BASE='deploy/'

def main():
    for path in PATHs:
        url = HOST + path
        print(url)
        r = requests.get(url, allow_redirects=True)
        file_name = DEPLOY_BASE + path
        print(file_name)
        file_d = open(file_name, 'wb')
        file_d.write(r.content)
        file_d.close()


if __name__ == '__main__':
    main()
