from bs4 import BeautifulSoup
from google import google
import requests

num_page = 1
def search_google(search_string):
    search_result = google.search(search_string+' in python -url"stack oveflow"',num_page)
    url = search_result[0].link
    scrape(url)
    return None

def scrape(url):
    url_obj_data  = requests.get(url)
    url_text_data = url_obj_data.text
    soup = BeautifulSoup(url_text_data,'html.parser')
    answer_element = soup.find("div", { "class" : "accepted-answer" })
    # print answer_element.prettify()
    pre = answer_element.findAll("pre")
    code =[]
    for x in pre:
        code.append(x.findAll("code"))
    for x in code:
        print x
    return None

search = raw_input("enter search string")
search_google(search)
