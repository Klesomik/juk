#TODO: sort order

from bs4 import BeautifulSoup
import requests

answer = {}
errors = []

def get_html(url):
    try:
        session = requests.Session()
        request = session.get(url)
        if request.status_code != requests.codes.ok:
           raise Exception('ERROR')
        return request.content
    except:
        raise Exception('ERROR')

def parse_faculty(url):
    print(url)
    try:
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        buffer = soup.find('tbody')
        buffer = buffer.find_all('tr')
        for it in buffer:
            res = it.find_all('td')
            res = res[3]
            res = str(res)
            res = res[4:-5]
            if res not in answer:
                answer[res] = []
            answer[res].append(url)
    except:
        errors.append(url)

def parse_university(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    buffer = soup.find_all('a')[1:]
    for a in buffer:
        link = url[:-10] + a.get('href')
        parse_faculty(link)

def parse_admlist():
    url = 'http://admlist.ru'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    buffer = soup.find_all('a')[2:]
    for a in buffer:
        link = url + '/' + a.get('href')
        parse_university(link)

def get_result_old(file_name):
    out = open(file_name, 'w')
    for name, data in answer.items():
        print(name, file=out)
        print('{', file=out)
        for link in data:
            print('\t' + link, file=out)
        print('}', file=out)
    print("=======================================================")
    print("totaly found {} students".format(len(answer)))

def get_result(file_name):
    buff = []
    for it in answer:
        buff.append(it)
    buff.sort()
    out = open(file_name, 'w')
    for name, data in buff:
        print(name, file=out)
        print('{', file=out)
        for link in data:
            print('\t' + link, file=out)
        print('}', file=out)
    print("=======================================================")
    print("totaly found {} students".format(len(buff)))

def print_errors():
    print('totaly found {} errors'.format(len(errors)))
    print(errors)

def main():
    parse_admlist()
    get_result_old('result_new.txt')
    print_errors()

if __name__ == '__main__':
    main()