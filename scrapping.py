import requests
from bs4 import BeautifulSoup
from re import sub
from myMongo import InsMongo
from datetime import datetime

COLLEGE_ROOT = 'http://edusanjal.com/college/'
mongodb = InsMongo()
# response = requests.get(college)
# soup = BeautifulSoup(response.text,'html.parser')

def get_college(url):
    print("COLLEGE_ROOT::",url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    colleges = soup.select('.detlsTitle a[href^="/college/"]')
    for college in colleges:
        parse_college(college['href'])
    mongodb.insert('visited',{'url':url,'date':datetime.now()})
    snext = soup.find('a',{'rel':'next'})['href']
    print(snext)
    get_college(COLLEGE_ROOT+snext)

def parse_college(vurl):
    print("COLLEGE_URL::",vurl)
    prefix = 'http://edusanjal.com/'
    response = requests.get(prefix+vurl)
    soup = BeautifulSoup(response.text,"lxml")
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
        'url':url
    }
    mongodb.insert('college',data)
    mongodb.insert('url',{'name':name, 'url':url, 'date':datetime.now()})
    mongodb.insert('visited',{'url':vurl, 'date':datetime.now()})



get_college(COLLEGE_ROOT)
