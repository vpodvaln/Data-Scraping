import time
from urllib.request import urlopen
from urllib.parse import urljoin
from lxml.html import fromstring
from lxml.etree import XMLSyntaxError
import xlsxwriter
from re import findall


START_URL = 'https://www.weblancer.net'
BASE_URL = 'https://www.weblancer.net/jobs/'
PAGE_URL = 'https://www.weblancer.net/jobs/?page='
Main_Path = 'div.container-fluid div.row'


def page_count():
    ListHtml = urlopen(BASE_URL).read()  # .decode("windows-1251")
    List_doc = fromstring(ListHtml)
    num_pages = List_doc.cssselect('ul.pagination li a')[-1]
    # latest_page = num_pages.get('href')[-3:]
    # return int(latest_page)
    latest_page = num_pages.get('href')
    latest_page_cut = findall(r'\d+', latest_page)
    return int(latest_page_cut[0])


def parse_all_page():
    all_jobs = []
    num_pages = page_count()
    print('Всего найдено страниц: %d' % num_pages)

    all_jobs.extend(parse_page(BASE_URL))
    for page in range(2, num_pages + 1):
        iter_page = parse_page(urljoin(PAGE_URL, str(page)))
        all_jobs.extend(iter_page)
        print("Парсинг %d%% страницы %d из %d)" % (page / num_pages * 100, page, num_pages))
    return all_jobs


def parse_page(URL):
    jobs = []
    ListHtml = urlopen(URL).read() # .decode("windows-1251")
    List_doc = fromstring(ListHtml)

    for project in List_doc.cssselect(Main_Path)[1:]:
        a = project.cssselect('.col-sm-7 a')[0]
        name = a.text
        href = a.get('href')
        url = urljoin(START_URL, href)

        try:
            price_path = project.cssselect('div.col-sm-1')[0]
            price = price_path.text.strip()
        except (AttributeError, IndexError):
            price = None


        try:
            offers_path = project.cssselect('div.col-sm-3')[0]
            offers = offers_path.text.strip()
        except (AttributeError, IndexError):
            offers = None

        try:
            desc_path = project.cssselect('div.col-xs-12')[0]
            desc = desc_path.text
        except (AttributeError, IndexError):
            desc = None

        try:
            categories_path = project.cssselect('a.text-muted')[0]
            categories = categories_path.text
        except (AttributeError, IndexError):
            categories = None

        try:
            date_path = project.cssselect('span span')[0]
            date = date_path.text
        except (AttributeError, IndexError):
            date = None


        jobs_data = {'name': name, 'url': url, 'price': price, 'offers': offers, 'desc': desc, 'categories': categories,'date': date}
        jobs.append(jobs_data)
        # time.sleep(1)

    return jobs


def save_excel(filename, array_jobs):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    field_name = ('Название', 'Цена', 'Заявки', 'Категория', 'Ссылка', 'Описание', 'Дата')
    bold = workbook.add_format({'bold': True})
    for row, name in enumerate(field_name):
        worksheet.write(0, row, name, bold)

    fields = ('name', 'price', 'offers', 'categories', 'url', 'desc',  'date')
    for row, name in enumerate(array_jobs, start=1):
        for col, field in enumerate(fields):
            worksheet.write(row, col, name[field])


def main():
    array_jobs = parse_all_page()
    save_excel('jobs_offers.xlsx', array_jobs)

    # pickle.dump(all_jobs, open('jobs_file.pickle', 'wb'))
    # json.dump(all_jobs, open('test.json', 'w'))


if __name__ == '__main__':
    main()

