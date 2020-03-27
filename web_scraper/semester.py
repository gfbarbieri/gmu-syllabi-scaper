from web_scraper.department import Department
from web_scraper.browser import Browser
from urllib import parse

class Semester(object):

    def __init__(self):
        self.department = Department()

    def find_semesters_available(self):
        #Two different full urls are needed to compile semesters available--they
        #only differ in the parameters used: code=ECON, and term=201907.
        url = "https://{}.gmu.edu".format(self.department.name)

        if self.department.name == 'economics':
            semester_url = parse.urljoin(url, 'course_sections')
            semester_parameters = [{'code':'ECON'}, {'term':'201970'}]

            available_semesters = []

            for parameter in semester_parameters:
                browser = Browser()
                response = browser.request(semester_url, parameters=parameter)
                soup = browser.soup(response)
                menu = soup.find_all('select', id='term-select')

                for sem in menu[0].find_all('option')[1:]:
                    available_semesters.append([sem.text, sem['value']])

                #Remove duplicate semester listings.
                available_semesters = list(dict(available_semesters).items())

        return available_semesters
