import time
from urllib.request import urlopen
from urllib.parse import urljoin
from lxml.html import fromstring
from lxml.etree import XMLSyntaxError
import xlsxwriter

START_URL = 'http://www.estateline.ru/companies/sales-production/noise-heat-insulation/'
URL_PAGE = 'http://www.estateline.ru/companies/sales-production/noise-heat-insulation/?stPage='
ITEM_PATH = 'tbody tr .name'
ADDRESS_PATH = '.profiler .rightProf .itemBox div'
PHONE_PATH = '.profiler .rightProf .itemBox div'
REGION_PATH = '.itemleft'
DESCR_PATH = '.profiler .rightProf .itemBox #aboutCompany'


def get_totalpages_number():
    f = urlopen(START_URL)
    list_html = f.read().decode('utf-8')
    list_doc2 = fromstring(list_html)
    return int(list_doc2.cssselect('div.paginator a')[-2].text_content())


def parse_pages():
    all_compan = []
    total_pages = get_totalpages_number()
    print('Всего найдено %d страниц...' % total_pages)

    all_compan.extend(parse_compan(START_URL))
    for page in range(2, total_pages + 1):
        print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        all_compan.extend(parse_compan(URL_PAGE + str(page)))
    return all_compan


def parse_compan(URL):
    compan = []
    f = urlopen(URL)
    list_html = f.read().decode('utf-8')
    list_doc = fromstring(list_html)

    try:
        for elem in list_doc.cssselect(ITEM_PATH):
            a = elem.cssselect('a.text')[0]
            href = a.get('href')
            name = a.text
            url = urljoin(URL, href)

            # time.sleep(1)
            details_html = urlopen(url).read().decode('utf-8')
            details_doc = fromstring(details_html)

            # time.sleep(1)
            region_elems = details_doc.cssselect(REGION_PATH)
            regions = [region_elem.text for region_elem in region_elems][1:]

            # time.sleep(1)
            address_elem = details_doc.cssselect(ADDRESS_PATH)[2]
            address = address_elem.text_content()

            # time.sleep(1)
            phone_elem = details_doc.cssselect(PHONE_PATH)[4]
            phones = phone_elem.text_content()

            # time.sleep(1)
            descr_elem = details_doc.cssselect(DESCR_PATH)[0]
            descr = descr_elem.text_content()

            # time.sleep(1)
            company = {'name': name, 'url': url, 'address': address, 'phones': phones, 'descr': descr,
                       'regions': regions}

            # time.sleep(1)
            compan.append(company)

            # time.sleep(1)

    except XMLSyntaxError:
        print('---XMLSyntaxError')
    except IndexError:
        print('---IndexError')
    return compan


def expor_excel(filename, compan):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    field_names = ('Название', 'Ссылка', 'Адрес', 'Телефон', 'Описание', 'Регион')
    bold = workbook.add_format({'bold': True})

    for col, field in enumerate(field_names):
        worksheet.write(0, col, field, bold)
    fields = ('name', 'url', 'address', 'phones', 'descr')

    for row, company in enumerate(compan, start=1):
        for col, field in enumerate(fields):
            worksheet.write(row, col, company[field])
        for regions in company['regions']:
            col += 1
            worksheet.write(row, col, regions)
    workbook.close()
    time.sleep(1)


def main():
    compan = parse_pages()
    expor_excel('compan.xlsx', compan)


if __name__ == '__main__':
    main()
