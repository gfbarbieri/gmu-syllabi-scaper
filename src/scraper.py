from bs4 import BeautifulSoup
import requests
import re
import os

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

    def make_request(self, url, params=None):
        """
        Performs GET requests.
        """

        try:
            response = requests.get(url, headers=self.headers, params=params)
        except Exception as e:
            raise e
        
        return response

    def content_parser(self, content, parser='html.parser'):

        soup = BeautifulSoup(markup=content, features=parser)

        return soup
    
class SyllabiScraper(Scraper):

    def __init__(self, base_url='https://economics.gmu.edu', term='202410'):
        super().__init__(base_url=base_url)
        self.term = term

    def request_terms(self):
        '''
        From the Geroge Mason website, return all semesters with data
        available from the dropdown menu.
        
        Returns a list of semesters.
        '''

        # Request and parse resulting HTML data.
        url = self.base_url + '/course_sections'
        response = self.make_request(url=url, params={'term': '202370'})
        html = self.content_parser(content=response.content)

        # Extract the list of terms.
        terms = (
            {
                term.text: term['value']
                for term in html.find_all('option') if term['value'] != ''
            }
        )

        return terms
    
    def request_courses(self):

        # Request course catalog page content.
        url = self.base_url + '/course_sections'
        response = self.make_request(url=url, params={'term': self.term})
        html = self.content_parser(content=response.content)

        # Extract courses and course details.
        metadata = (
            [
                self.extract_course_details(course_content=course)
                for course in html.find_all('div', {'class': 'course content'})
            ]
        )

        return metadata
    
    def request_sections(self, course):

        # Request course page content.
        url = self.base_url + course['partial_url']
        response = self.make_request(url=url, params={'term': self.term})
        html = self.content_parser(content=response.content)

        # Extract course section's number and URL.
        section_urls = []
        
        for section in html.find('h2').findNext('ul').find_all('li'):
            section_urls.append({
                'number': os.path.split(section.find('a')['href'])[1],
                'partial_url': section.find('a')['href']
            })
    
        return section_urls
    
    def request_section_details(self, section):
        
        # Request section page content.
        url = self.base_url + section['partial_url']
        response = self.make_request(url=url, params={'term': self.term})
        html = self.content_parser(content=response.content)

        # Extract section syllabus URL and instructor from the sidebar.
        sidebar = html.find('aside', {'id': 'sidebar'})
        syllabus_url = sidebar.find('h2').findNext('a')['href']
        instructor = sidebar.find('h2').findNext('h2').findNext('a').text

        return instructor, syllabus_url
    
    def request_syllabus(self, section):

        # Request syllabus content.
        url = section['syllabus_url']
        response = self.make_request(url=url)

        return response.content

    def extract_course_details(self, course_content):

        course_details = {}

        # Format course header.
        formatted_title = re.sub(' +', ' ', course_content.find('h3').text.replace('\n', ''))
        
        # Create a regex pattern from the formatted title.
        pattern = re.compile(r"ECON\s+(\d+):\s+(.*?)\s+\((\d+)(?:-(\d+))?\s+Credits\)")

        # Use the pattern to parse the formatted title. Extract course number,
        # course title and course credits.
        match = pattern.search(formatted_title)
        course_details['number'] = match.group(1)
        course_details['title'] = match.group(2)
        course_details['credits'] = match.group(3)

        # Extract course description.
        course_details['description'] = course_content.find('div', {'class': 'courseblockdesc'}).text

        # Create course partial URL.
        course_details['partial_url'] = f"/courses/econ{course_details['number']}"

        return course_details