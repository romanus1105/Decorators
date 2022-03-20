#!/usr/bin/env python3

import requests
import bs4
import sys
import logging

def logger(old_function):
    def new_fuction(*args, **kwargs):
        result = old_function(*args, **kwargs)
        logging.info(f"Arguments: {args} {kwargs} - Return: {type(result)}")
        return result
    return new_fuction

def article_parser(url, keywords_list):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url=url, headers=user_agent)
    except:
        print('Failed to connect to server. Check your Internet connection.')
        sys.exit()
    if res.status_code == 200:
        res.raise_for_status()
        text = res.text
        soup = bs4.BeautifulSoup(text, features='html.parser').find(class_='article-formatted-body')
        paragraphs = soup.find_all('p')
        words = []
        for paragraph in paragraphs:
            for word in paragraph.text.split():
                words.append(word)
        for word in keywords_list:
            if word in words:
                return True
    else:
        print(f'Failed to complete your request. Response status code - {res.status_code}')
    return False

def check_articles(articles, keywords_list, url):
    for article in articles:
        href = article.find(class_='tm-article-snippet__title-link').attrs['href']
        article_url = f'{url + href}'
        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs = set(hub.text.strip() for hub in hubs)
        for hub in hubs:
            if hub in keywords_list:
                title = article.find('h2').find('span').text
                datetime = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title'].split(',')[0]
                print(f'{datetime} - {title} - {url + href}')
                break
            else:
                if article_parser(url=article_url, keywords_list=keywords_list):
                    title = article.find('h2').find('span').text
                    datetime = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title'].split(',')[0]
                    print(f'{datetime} - {title} - {url + href}')
                    break

@logger
def get_articles(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url=f'{url}/ru/all/', headers=user_agent)
    except:
        print('Failed to connect to server. Check your Internet connection.')
        sys.exit()
    if res.status_code == 200:
        res.raise_for_status()
        text = res.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all('article')
        return articles
    else:
        print(f'Failed to complete your request. Response status code - {res.status_code}')

def main():
    KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'Информационная безопасность *', 'Raspberry']
    url = 'https://habr.com'
    log_file = input('''Enter the full path to log file (Ex.: tmp.log): ''')
    log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s - %(message)s"
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_format)
    articles = get_articles(url=url)
    check_articles(articles=articles, keywords_list=KEYWORDS, url=url)

if __name__ == '__main__':
    main()