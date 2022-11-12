import requests
import bs4
import datetime
from functools import wraps


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ym_d=1628840683; _ym_uid=1628840683355101683; _ga=GA1.2.137596937.1628841988; fl=ru; hl=ru; feature_streaming_comments=true; _gid=GA1.2.1021543475.1641571984; habr_web_home=ARTICLES_LIST_ALL; _ym_isad=1; visited_articles=599735:203282; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1',
    'Host': 'habr.com',
    'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping',
    'sec-ch-ua': '"Chromium";v="94", "Yandex";v="21", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'}

MY_FAVORITES = {'софт', 'читальный зал', 'здоровье', 'python'}


def decorator(log_way):
    def _decorator(some_func):
        @wraps(some_func)
        def new_func(*args, **kwargs):
            res = some_func(*args, **kwargs)
            tm = datetime.datetime.now()
            print1 = f'function named "{make_req.__name__}" was called at {tm} with args: {args} and {kwargs}\n'
            print2 = f'result = {res}'
            with open(log_way, 'w', encoding='Utf-8') as logfile:
                logfile.write(print1)
                logfile.write(print2)
            return res
        return new_func
    return _decorator


@decorator(log_way='D:\\pycharmTests\\HW Decorators\\log.txt')
def make_req(HEADERS, FAVORITES):
    resp = requests.get('https://habr.com/ru/all/', headers=HEADERS)
    resp.raise_for_status()
    text = resp.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article', class_='tm-articles-list__item')
    for article in articles:
        hubs = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
        hubs = set(hub.find('span').text.strip().lower() for hub in hubs)
        date = article.find('time').text
        title = article.find('a', class_='tm-article-snippet__title-link')
        span_title = title.find('span').text
        if FAVORITES & hubs:
            href = title['href']
            url = 'https://habr.com' + href
            result = f'Дата: {date} - Заголовок: {span_title} - Ссылка: {url}'
            print(result)
            return result

if __name__ == '__main__':
    make_req(HEADERS, MY_FAVORITES)