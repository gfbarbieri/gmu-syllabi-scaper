# Web Scraping Course syllabi
Web scraping George Mason University's Department of Economics website for all course syllabi.

### Author:
Greg Barbieri - [gfbarbieri](https://github.com/gfbarbieri)

## Description
The goal of this project is to obtain the syllabi for courses offered in the Economics Department at George Mason University.

### Folder Organization
data: Data resulting from ingestion and wrangling process. The data ingested are the HTML for all of the courses listed for the semesters available on the Economics Department's course and syllabi website. The HTML is a dictionary, output as a Pickle file, which has the semester, the page URL, and course page contents as a Request object. The result of the wrangling process are course syllabi for each course where a syllabus was posted.  
notebooks: The final notebook covering all the functions needed--mostly a sandbox.  
src: Ingestion and wrangling Python program files.

## Data Sources
HTML Data is pulled from George Mason University, [Economics Department](https://economics.gmu.edu)
