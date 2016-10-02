import requests
from bs4 import BeautifulSoup
from re import sub


college = 'http://edusanjal.com/college/'
# response = requests.get(college)
# soup = BeautifulSoup(response.text,'html.parser')

def get_college(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    colleges = soup.select('.detlsTitle a[href^="/college/"]')
    for college in colleges:
        parse_college(college['href'])
    snext = soup.find('a',{'rel':'next'})['href']
    print(snext)
    get_college(college+snext)

def parse_college(url):
    prefix = 'http://edusanjal.com/'
    response = requests.get(prefix+url)
    soup = BeautifulSoup(response.text,"lxml")
    name = sub(ur'\s+',' ', soup.find('h1',{'class':'mainHeading'}).get_text())
    location  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-map-marker'}).parent.span.get_text())
    university  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-university'}).parent.get_text())
    contact  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-phone'}).parent.get_text())
    email  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-envelope-o'}).parent.get_text())
    url  =  sub(ur'\s+',' ', soup.find('i',{'class':'fa-external-link'}).parent.get_text())


get_college(college)
