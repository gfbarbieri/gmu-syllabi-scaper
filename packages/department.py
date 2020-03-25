import requests
from bs4 import BeautifulSoup

'''
department, semester, course, syllabus
what does department have?
department has what? Department has a function called get semesters.
'''
class Department(object):

    def __init__(self, dept='economics', params={'term': '201970'}):
        self.dept = dept
        self.params = params
        self.headers = {'User-Agent': 'Chrome/74.0.3729.169'}
        self.url = "https://{}.gmu.edu".format(self.dept)

class Semester(object):

    def __init__(self):
        self.semesters = []
        self.department = Department()

    def set_semesters(self, fetch='all'):
        '''
        From the Geroge Mason website, return all semesters with data available
        from the dropdown menu. Returns a list of values which represent a semester.
        '''
        #Make request
        self.url = requests.compat.urljoin(self.department.url, '/course_sections')

        try:
            response = requests.get(self.url, headers=self.department.headers, params=self.department.params)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        #Parse resulting HTML data.
        soup = BeautifulSoup(response.text)

        #Semesters available are those available thourhg the drop-down menu. Search
        #for drop-down menu options.
        avail_semesters = soup.find_all('select', id='term-select')

        #Loop over each option in the drop-down menu. For each option, determine
        #the code for the website url and its text
        #name. [1:] removes the default menu title "Choose a term".
        for sem in avail_semesters[0].find_all('option')[1:]:
            if fetch == 'all':
                self.semesters.append([sem['value'], sem.text])
            elif sem.text == fetch:
                self.semesters = [sem['value'], sem.text]

        return self.semesters
