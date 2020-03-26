#import requests
#from bs4 import BeautifulSoup

from web_scraper.department import Department

class Semester(object):

    def __init__(self):
        self.semesters = None
        self.department = Department()

    def find_semesters_available(self):
        #Two different full urls are needed to compile a complete list of the semesters available
        #on the GMU Economics Department website--they only differ in the parameters
        #used: https://economics.gmu.edu/course_sections?code=ECON, and
        #https://economics.gmu.edu/course_sections?term=201907.
        if self.department.dept == 'economics':
            course_section_url = requests.compat.urljoin(self.department.url, '/course_sections')
            course_parameters = [{'code':'ECON'}, {'term':'201970'}]

        available_semesters = []

        #For each of the two course parameters, we want to search the semesters
        #available by finding the dropdown menu on the GMU website where users
        #can select which semester to view courses for and extracting the text users
        #see when selecting a semester.
        for parameter in course_parameters:
            #Find future, current, or past semesters available.
            try:
                response = requests.get(course_section_url, headers=self.department.headers, params=parameter)
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features='lxml')
                menu = soup.find_all('select', id='term-select')

                for sem in menu[0].find_all('option')[1:]:
                    available_semesters.append([sem.text, sem['value']])

        return available_semesters

    def set_semester(self, sem='Fall 2019'):
        '''
        The goal is to set self.semester, which a forthcoming class will use to pull the correct
        course contents.
        '''

        #From available semesters, find the HTML parameter value that matches
        #the user defined semester.
        available_semesters = find_semesters_available()
