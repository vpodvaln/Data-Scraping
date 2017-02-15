import time
from urllib.request import urlopen
from urllib.parse import urljoin
from lxml.html import fromstring
from lxml.etree import XMLSyntaxError
import xlsxwriter
import csv

URL_COURSE = "https://geekbrains.ru/courses#free"
START_URL = "https://geekbrains.ru"

Main_Path = ".col-md-6 .course-item__description"
Course_Information_Path = ".main-content div.padder-v"
Review_Course_Path = "div.m-b-xs"
Author_Patch = "ul.nav-pills li div.pull-left p"


def parse_courses():

    courses_array = []
    ListHtml = urlopen(URL_COURSE).read().decode("utf-8")
    List_doc = fromstring(ListHtml)

    try:
        for elem in List_doc.cssselect(Main_Path):
            a = elem.cssselect('a.course-item__description__title')[0]
            href = a.get('href')
            name = a.text
            url = urljoin(START_URL, href)

            # time.sleep(2)

            details_html = urlopen(url).read().decode('utf-8')
            details_doc = fromstring(details_html)
            CourseInfo = details_doc.cssselect(Course_Information_Path)[0]

            Review_Course = CourseInfo.cssselect(Review_Course_Path)[0]
            review = Review_Course.text_content()

            Author_Course = CourseInfo.cssselect(Author_Patch)[0:]
            author = [auth.text_content() for auth in Author_Course]

            course_datta = {'name': name, 'review': review, 'author': author, 'url': url}
            courses_array.append(course_datta)

    except XMLSyntaxError:
        print('---XMLSyntaxError')
    except IndexError:
        print('---IndexError')
    return courses_array


def export_excel(filename, courses):

    # Create csv file
    workboock = xlsxwriter.Workbook(filename)
    worksheet = workboock.add_worksheet()

    # Write row-name in csv file
    bold = workboock.add_format({'bold': True})
    field_names = ('Imya', 'Opisanie', 'Url', 'Avtor')
    for col, field in enumerate(field_names):
        worksheet.write(0, col, field, bold)

    # Write all array in csv file
    fields = ('name', 'review', 'url')
    for row, cours in enumerate(courses, start=1):
        for col, field in enumerate(fields):
            worksheet.write(row, col, cours[field])
        for auth in cours['author']:
            col += 1
            worksheet.write(row, col, auth)

    workboock.close()


def save_csv(filename, courses):
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Imya', 'Opisanie', 'Avtor', 'Url'))

        for cours in courses:
            writer.writerow((cours['name'], cours['review'], cours['author'], cours['url'], ))


def main():
    courses = parse_courses()
    # courses = []
    export_excel('courses.xlsx', courses)
    # save_csv('coursee.csv', courses)

if __name__ == '__main__':
    main()

