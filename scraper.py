from lxml import html
import requests

def scrapeLink(query,lang):
    # query="aditya l1 launch"
    # lang='en'
    URL = f'https://news.google.com/search?q={query}&hl={lang}'
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(URL, headers=HEADERS)

    print(webpage)

    tree = html.fromstring(webpage.content)
    result = []

    for i in range(12):
        anchor_tags = tree.xpath(f'//main/c-wiz/div[1]/div[{i}]/div/article/a')
        for tag in anchor_tags:
            # print(tag.text_content())
            # print("https://news.google.com"+tag.get('href').split('.')[1])
            response = requests.get("https://news.google.com"+tag.get('href').split('.')[1], allow_redirects=False)
            if response.status_code == 301:
                redirected_url = response.headers['Location']
                # print("Final Redirected URL:", redirected_url)
                result.append(redirected_url)
    return result



