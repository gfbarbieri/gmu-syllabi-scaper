from scraper import SyllabiScraper
import os

def main():
    # Set term.
    term = 'Spring 2024'

    # Initialize scraper.
    gmus = SyllabiScraper()
    print(f"Syllabi scraper initialized with term: {gmus.term}")

    # Request terms available in the course catalog.
    print("Searching available terms.")
    avail_terms = gmus.request_terms()
    print(f"Terms available: {len(avail_terms)}.")

    # Choose a term.
    print(f"Term selected: {term} ({avail_terms[term]}).")
    gmus.term = avail_terms[term]

    ###########################################################################
    # GET COURSE CATALOG
    ###########################################################################

    # Request the course catalog for the term.
    print(f"Requesting course catalog for {gmus.term}.")
    courses = gmus.request_courses()
    print(f"The number of courses scheduled for {gmus.term}: {len(courses)}.")

    # For each course offered in the term, extract the URL for each section
    # of the course.
    for course in courses:
        print(f"Request sections for course: {course['title']}.")
        course['sections'] = gmus.request_sections(course=course)
        print(f"The number of course sections offered: {len(course['sections'])}")

    ###########################################################################
    # GET SECTION DETAILS
    ###########################################################################

    # For each course section, extract the URL for the syllabus and the
    # section's instructor.
    for course in courses:
        print(f"Starting course: {course['title']}")
        
        for section in course['sections']:
            print(f"Starting section: {section['number']}")
            section['instructor'], section['syllabus_url'] = gmus.request_section_details(section=section)
            print(f"Instructor: {section['instructor']}, Syllabus: {section['syllabus_url']}")
            print(f"Section completed: {section['number']}")

        print(f"Course completed: {course['title']}")

    ###########################################################################
    # DOWNLOAD SYLLABI
    ###########################################################################
        
    # For each course section, download the instructor's course syllabus.
    for course in courses:
        print(f"Starting course: {course['title']}")
        
        for section in course['sections']:
            print(f"Starting section: {section['number']}")

            # Get syllabus from URL.
            syllabus = gmus.request_syllabus(section=section)

            # Create file path.
            print(f"Veryfiying file path.")

            folder = f"../data/{term}"
            file_name = f"ECON_{course['number']}_{course['title'].replace(' ','_')}_{section['number']}_{section['instructor'].split()[-1]}.pdf"
            file_path = os.path.join(folder, file_name)

            if not os.path.exists(folder):
                os.makedirs(folder)

            # Write syllabus to file path.
            with open(file_path, 'wb') as f:
                f.write(syllabus)

            print(f"Instructor: {section['instructor']}, Syllabus: {section['syllabus_url']}")
            print(f"Section completed: {section['number']}")

        print(f"Course completed: {course['title']}")