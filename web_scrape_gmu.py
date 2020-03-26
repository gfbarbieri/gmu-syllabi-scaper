from web_scraper.semester import Semester

example = Semester()
semesters_available = example.find_semesters_available()
print(len(semesters_available), semesters_available)
