import requests
from bs4 import BeautifulSoup
from re import sub
from myMongo import CMongoDB
from datetime import datetime

COLLEGE_ROOT = 'http://edusanjal.com/college/'
mongodb = CMongoDB()
Parse = []
# response = requests.get(college)
# soup = BeautifulSoup(response.text,'html.parser')
def get_parsed():
    print list(mongodb.get('edusanjal_parsed_colleges'))

def get_college(skip=0,limit=6000):
    colleges = mongodb.get('college',skip=skip,limit=limit)
    for college in colleges:
        page = college['soup']
        soup = BeautifulSoup(page,"lxml")
        try:
            parse_college(soup)
            mongodb.insert('edusanjal_parsed_colleges',{'id':college['_id'], 'date':datetime.now()})
        except:
            continue

def parse_college(soup):
    try:
        name = sub(ur'\s+',' ', soup.find('h1',{'class':'mainHeading'}).get_text())
    except Exception as e:
        name = ""
    try:
        location  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-map-marker'}).parent.span.get_text())
    except Exception as e:
        location = ""
    try:
        university  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-university'}).parent.get_text())
    except Exception as e:
        university = ""
    try:
        contact  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-phone'}).parent.get_text())
    except Exception as e:
        contact = ""
    try:
        email  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-envelope-o'}).parent.get_text())
    except Exception as e:
        email = ""
    try:
        url  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-external-link'}).parent.get_text())
    except Exception as e:
        url = ""
    data= {
        'name':name,
        'location':location,
        'university':university,
        'contact':contact,
        'email':email,
        'url':url,
        'date': datetime.now()
    }
    mongodb.insert('edusanjal_colleges',data)

get_college(skip=0)
#
# get_parsed()
