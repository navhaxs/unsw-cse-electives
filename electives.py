#!/usr/bin/env python3
from lxml import html
import requests

page = requests.get("http://www.handbook.unsw.edu.au/vbook2017/brCoursesBySubjectArea.jsp?studyArea=COMP&StudyLevel=Undergraduate")
tree = html.fromstring(page.content)

# with open("raw.html","r") as in_file:
#     raw_html = in_file.read()
#tree = html.fromstring(raw_html)

print("# CSE Electives\n\n")

s1_offered = []
s2_offered = []
not_offered = []

# for each of the two tables (breadth and depth)
j = 0
elements = tree.find_class("tabluatedInfo")
table = elements[0]
for row in table:

    row_elements = row.xpath('td')
    if len(row_elements) == 3:
        course_code = row_elements[0].text
        course_title = row_elements[1].xpath('a')[0].text

        j = j + 1

        timetable_url = requests.get("http://timetable.unsw.edu.au/2017/" + course_code + ".html")

        subtree = html.fromstring(timetable_url.content)

        e = subtree.xpath('.//*[contains(text(),"offering information for the selected course was not found")]')
        if (len(e) > 0):
            not_offered.append([course_code, course_title])
        else:
            e = subtree.xpath('.//*[contains(text(),"SEMESTER ONE")]')
            if (len(e) > 0):
                s1_offered.append([course_code, course_title])
            e = subtree.xpath('.//*[contains(text(),"SEMESTER TWO")]')
            if (len(e) > 0):
                s2_offered.append([course_code, course_title])

print("\n### Offered 2017s1:")
for i in s1_offered:
    print('[{0}](http://timetable.unsw.edu.au/2017/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2017/{0}.html)\n'.format(i[0], i[1]))

print("\n### Offered 2017s2:")
for i in s2_offered:
    print('[{0}](http://timetable.unsw.edu.au/2017/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2017/{0}.html)\n'.format(i[0], i[1]))

print("\n### Not running :(")
for i in not_offered:
    print('[{0}](http://timetable.unsw.edu.au/2017/{0}.html) [{1}](http://www.handbook.unsw.edu.au/undergraduate/courses/2017/{0}.html)\n'.format(i[0], i[1]))

