import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


keywords = ['дизайн', 'фото', 'web', 'python']
# Иногда в ленте нету совподений, ниже набор для тестов
# keywords = ['сколько', 'занимают', 'прод', 'sql', 'node.js', 'java', 'web', 'python']


def post_parsing(keywords):
    response = requests.get('https://habr.com/ru/all/')
    text = response.text

    soup = BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')

    for article in articles:
        title = [t.text.strip() for t in article.find_all('h2')][0]
        date_post = [t.text.strip() for t in article.find_all('span', class_="post__time")][0]
        url_post = article.find('a', class_='btn btn_x-large btn_outline_blue post__habracut-btn').get('href')

        # Ищем совпадение по всей статье
        full_text(url_post, date_post, title, keywords)


# Ищем совпадение по всей статье
def full_text(url, date_post, title, keywords):
    response = requests.get(url)
    text = response.text

    soup = BeautifulSoup(text, features='html.parser')
    full_text_post = [t.text.strip() for t in soup.find_all('div', class_='post__body post__body_full')][0].lower()

    for word in keywords:
        if word in full_text_post:
            print(f'<{data_time(date_post)}> - <{title}> - <{url}>')
            break


# Если пост создан сегодня, то ставит сегодняшнюю дату числом(дд-мм-гг) а время(чч:мм) с поста
# Если статья вчерашняя, то от сегодня - 1 day
def data_time(string):
    if 'сегодня' in string:
        date = datetime.now()
        return str(date.strftime("%d.%m.%Y")) + ' ' + string[-1:-6:-1][-1::-1]
    elif 'вчера' in string:
        date = datetime.now() - timedelta(days=1)
        return str(date.strftime("%d.%m.%Y")) + ' ' + string[-1:-6:-1][-1::-1]


if __name__ == '__main__':
    post_parsing(keywords)
