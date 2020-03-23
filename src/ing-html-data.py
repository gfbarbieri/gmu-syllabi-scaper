import os
import pickle
import requests

from bs4 import BeautifulSoup

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

def build_semester_list():
    '''
    From the Geroge Mason website, return all semesters with data available
    from the dropdown menu. Returns a list of values which represent a semester.
    '''
    #Make default request.
    response = make_request()

    #Parse resulting HTML data.
    soup = BeautifulSoup(response.text)

    #Semesters available are those available thourhg the drop-down menu. Search
    #for drop-down menu options.
    avail_semesters = soup.find_all('select', id='term-select')

    #Loop over each option in the drop-down menu. For each option, determine
    #the code for the website url and its text
    #name. [1:] removes the default menu title "Choose a term".
    semesters = []

    for sem in avail_semesters[0].find_all('option')[1:]:
        semesters.append([sem['value'], sem.text])

    return semesters

def download_html(semesters, directory, file_name):
    '''
    Download the HTML using the Requests library. User supplied list has
    parameters needed for the make_requests function. Returns a dictionary, but
    also saves the dictoinary as a Pickle file in a user-defined directory.
    '''
    semester_html_data = {}

    #Download GMU Website HTML for each semester, store in a dictionary.
    for sem_value, sem_string in semesters:
        params = {'term': sem_value}
        response = make_request(params=params)

        #Replace "Fall 2019" with "Fall_2019", it helps later if one wants to
        #use it as a file name.
        sem_string = sem_string.replace(' ','_')
        semester_html_data[sem_string] = {}
        semester_html_data[sem_string]['value'] = sem_value
        semester_html_data[sem_string]['url'] = response.url
        semester_html_data[sem_string]['response'] = response

    #Create directory if directory does not exist.
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Save the resulting dictionary as a Pickle file.
    file_path = os.path.join(directory, file_name)

    #Write dictionary as Pickle file.
    with open(file_path,'wb') as file:
        pickle.dump(semester_html_data, file)

def main():
    semester_list = build_semester_list()
    semester_test = semester_list[:1]

    directory = os.path.join('..','data','html-data')
    file_name = 'gmu-semester-html.pickle'
    download_html(semesters=semester_test, directory=directory, file_name=file_name)

if __name__ == '__main__':
    main()
