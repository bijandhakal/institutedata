import crawerl
import logging
import logging.config
from myMongo import CMongoDB
from datetime import datetime
import threading

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('crawlerLogger')
mongodb = CMongoDB()

ROOT = {}
ROOT['COLLEGE'] = 'http://edusanjal.com/college/'
ROOT['UNIVERSITY'] = 'http://edusanjal.com/university/'
ROOT['COURSE'] = 'http://edusanjal.com/course/'
EDUSANJAL = 'http://edusanjal.com'
visitedCollege = []
visitedCollegePagination = []
visitedCourse = []
visitedCoursePagination = []

def handle_college(page_url):
    Spage = crawerl.init(page_url)
    if not page_url in visitedCollegePagination:
        colleges = Spage.select('.detlsTitle a[href^="/college/"]')
        for college in colleges:
            name = college['href'].split('/')[-1]
            college_url = EDUSANJAL + college['href']
            if not college_url in visitedCollege:
                soup = crawerl.init(college_url)
                page = soup.find('div',{'class':'content_all'})
                data = {
                    'url' : college_url,
                    'name': name,
                    'soup' : str(page),
                    'date' : datetime.now()
                }
                mongodb.insert('college',data)
            else:
                logger.info("VISITED :: {}".format(college_url))
        mongodb.insert('collegePagination',{'url':page_url,'date' : datetime.now()})
    else:
        logger.info("VISITED :: {}".format(page_url))
    nextPage = getNext(Spage)
    handle_college(ROOT['COLLEGE']+nextPage)

def handle_course(page_url):
    Spage = crawerl.init(page_url)
    if not page_url in visitedCoursePagination:
        courses = Spage.select('.detlsTitle a[href^="/course/"]')
        for course in courses:
            name = course.get_text()
            course_url = EDUSANJAL + course['href']
            if not course_url in visitedCourse:
                soup = crawerl.init(course_url)
                page = soup.find('div',{'class':'content_all'})
                data = {
                    'url' : course_url,
                    'name' : name,
                    'page' : str(page),
                    'date' : datetime.now()
                }
                mongodb.insert('course',data)
            else:
                logger.info("VISITED :: {}".format(course_url))
        mongodb.insert('coursePagination',{'url':page_url,'date' : datetime.now()})
    else:
        logger.info("VISITED :: {}".format(page_url))
    nextPage = getNext(Spage)
    handle_course(ROOT['COURSE']+nextPage)

def getVisitedCollege():
    colleges = mongodb.get('college',projection = {'url':True,'_id':False})
    pages = mongodb.get('collegePagination',projection = {'url':True,'_id':False})
    for college in colleges:
        visitedCollege.append(college['url'])
    for page in  pages:
        visitedCollegePagination.append(page['url'])

def getVisitedCourse():
    courses = mongodb.get('course',projection = {'url':True,'_id':False})
    pages = mongodb.get('coursePagination',projection = {'url':True,'_id':False})
    for course in courses:
        visitedCourse.append(course['url'])
    for page in  pages:
        visitedCoursePagination.append(page['url'])

def getNext(soup):
    snext = soup.find('a',{'rel':'next'})['href']
    return snext

if __name__ == '__main__':
    getVisitedCourse()
    getVisitedCollege()
    try:
        course_thread = threading.Thread(target=handle_course, args = ( ROOT['COURSE'], ) )
        course_thread.start()
        college_thread = threading.Thread(target=handle_college, args = ( ROOT['COLLEGE'], ) )
        college_thread.start()
    except:
       print "Error: unable to start thread"
