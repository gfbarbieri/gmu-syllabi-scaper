import os
import pickle
import requests

from bs4 import BeautifulSoup

def load_html(path):
    '''
    Load HTML data.
    '''
    with open(path,'rb') as file:
        html_dict = pickle.load(file)

    return html_dict

def edit_text(text):
    '''
    Edit text, specifically the course titles from various link and header sections of the HTML.
    '''
    text = (text.strip()
            .replace(':','')
            .replace(',','')
            .replace('\'','')
            .replace(' ','_')
            .replace('&','')
            .replace('.',''))

    return text

def course_title_parser(html):
    '''
    Takes the course block and parses out and returns the course title.
    '''
    #Parse HTML for header section.
    course_header = html.find('header').text.split('\n')
    course_header_title = course_header[2]

    #Initially, set course title is to the course title parsed from the course header.
    course_title = edit_text(course_header_title)

    #If the course title parsed from the header is "Special Topics in Economics", then instead of using
    #the course title parsed from the header, update the course title to the course title parsed from
    #the links for each individual section of the course offered.
    if course_title == 'Special_Topics_in_Economics':
        course_links = html.find_all('a')
        for link in course_links:
            if len(link.text.split(':')) > 1:
                course_title = edit_text(link.text.split(':')[1])

    return course_title

def course_syllabi_parser(html):
    '''
    Parse the HTML for a course syllabus URL.
    '''
    course_links = html.find_all('a')

    course_syllabus_link = []

    for link in course_links:
        if link.text == "Section Syllabus":
            has_syllabus = True
            pdf_url = 'https:{}'.format(link['href'].split("?")[0])
            pdf_params = link['href'].split("?")[1]
            pdf_file_name = os.path.basename(pdf_url)
            course_syllabus_link.append([pdf_file_name, pdf_url, pdf_params])

    return course_syllabus_link

def compile_course_syllabi(html_dict):
    '''
    Comple course titles, syllabi url details, and file names. Returns a list with each course section syallbus as
    an element associated with the course title.
    '''
    gmu_econ_syllabi = []

    #For each semester and course block, find each course title and course syllabus for each course section.
    for semester, course_block in html_dict.items():
        block_soup = BeautifulSoup(course_block['response'].text)
        sem_course_content = block_soup.find_all('div', class_='course content')

        for course in sem_course_content:
            #Parse the course content for the course title.
            course_title = course_title_parser(course)

            #Parse course content for the url to the course syllabus.
            course_syllabi = course_syllabi_parser(course)

            #Append course title and syllabus details to list.
            gmu_econ_syllabi.append([semester, course_title, course_syllabi])

    return gmu_econ_syllabi

def make_request(url="https://economics.gmu.edu/course_sections",
                 headers={'User-Agent': 'Chrome/74.0.3729.169'},
                 params={'term': '201970'},
                 print_info=False):
    '''
    Submits a GET request using the Requests library for a given URL. Default
    values are from George Mason Economics Department website. Returns a
    Request object.
    '''
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if print_info == True:
        print(response.url, response.status_code)

    return response

def download_syllabi(directory, file_name, url, params):
    '''
    Download syllabus at the url and save it to the user-defined directory.
    '''
    #Create directory if directory does not exist.
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Save the resulting dictionary as a Pickle file.
    file_path = os.path.join(directory, file)

    #Download PDFs.
    response_pdf = make_request(url=url, params=params)

    #Write to drive.
    with open(file_path, "wb") as pdf:
        for chunk in response_pdf.iter_content():
            pdf.write(chunk)

def main():
    path = os.path.join('..', 'data', 'html-data', 'gmu-semester-html.pickle')
    gmu_html_dict = load_html(path)

    gmu_syllabi_list = compile_course_syllabi(gmu_html_dict)

    for semester, course_title, syllabi in gmu_syllabi_list:
        for syllabus in syllabi:
            out_dir = os.path.join('..', 'data','gmu-syllabi', course_title, semester)
            download_syllabi(directory=out_dir, file_name=syllabus[0], url=syllabus[1], params=syllabus[2])

if __name__ == '__main__':
    main()
