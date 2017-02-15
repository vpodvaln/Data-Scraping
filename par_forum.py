import time
from urllib.request import urlopen
from urllib.parse import urljoin
from lxml.html import fromstring
import xlsxwriter

URL = 'http://www.estateline.ru/companies/sales-production/noise-heat-insulation/'
ITEM_PATH = 'tbody tr .name'
ADDRESS_PATH = '.profiler .rightProf .itemBox div'
PHONE_PATH = '.profiler .rightProf .itemBox div'
REGION_PATH = '.itemleft'
DESCR_PATH = '.profiler .rightProf .itemBox #aboutCompany'


def parse_compan():
    compan = []

    # URL Open
    f = urlopen(URL)
    list_html = f.read().decode('utf-8')
    list_doc = fromstring(list_html)

    for elem in list_doc.cssselect(ITEM_PATH):
        a = elem.cssselect('a.text')[0]
        href = a.get('href')
        name = a.text
        url = urljoin(URL, href)
        #time.sleep(1)

        # URL Open
        details_html = urlopen(url).read().decode('utf-8')
        details_doc = fromstring(details_html)

        region_elems = details_doc.cssselect(REGION_PATH)[0]
        regions = [region_elem.text for region_elem in region_elems][1:]
        print(regions)

        address_elem = details_doc.cssselect(ADDRESS_PATH)[2]
        address = address_elem.text_content()

        phone_elem = details_doc.cssselect(PHONE_PATH)[4]
        phones = phone_elem.text_content()

        descr_elem = details_doc.cssselect(DESCR_PATH)[0]
        descr = descr_elem.text_content()


        company = {'name': name, 'url': url, 'address': address, 'phones': phones, 'descr': descr, 'regions': regions}

        compan.append(company)
    return compan


def expor_excel(filename, compan):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    field_names = ('Название', 'Ссылка', 'Адрес', 'Телефон', 'Описание', 'Регион')

    for i, field in enumerate(field_names):
        worksheet.write(0, i, field)
    fields = ('name', 'url', 'address', 'phones', 'descr')

    for row, company in enumerate(compan, start=1):
        for col, field in enumerate(fields):
            worksheet.write(row, col, company[field])
        for regions in company['regions']:
            col += 1
            worksheet.write(row, col, regions)

    workbook.close()


# def main():
#     compan = parse_compan()
#     expor_excel('compan.xlsx', compan)
#
#
# if __name__ == '__main__':
#     main()

