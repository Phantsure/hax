#These two files have to be downloaded to run this code
#pip install Google_Search_API-1.1.13-py2-none-any.whl
#pip install beautifulsoup4-4.6.0-py2-none-any.whl
from bs4 import BeautifulSoup
from google import google
import requests

num_page = 1
def search_google(search_string):#searching str
    search_result = google.search(search_string+' in python -url"stack oveflow"',num_page)
    url = search_result[0].link
    scrape(url)
    return None

def scrape(url):#extracting data
    url_obj_data  = requests.get(url)
    url_text_data = url_obj_data.text
    soup = BeautifulSoup(url_text_data,'html.parser')
    answer_element = soup.find("div", { "class" : "accepted-answer" })
    # print answer_element.prettify()
    #this is the Error with this print statement
    # encode return codecs.charmap_encode(input,errors,encoding_map)
    # UnicodeEncodeError: 'charmap' codec can't encode character u'\u2013' in position 5888: character maps to <undefined>
    pre = answer_element.findAll("pre")
    code =[]
    for x in pre:
        code.append(x.findAll("code"))
    for x in code:
        for i in x:
            print x.text()#print x works(But differentely not as wanted)
#This is the Error to be cured
#ResultSet object has no attribute '%s'. You're probably treating a list of items like a single item. Did you call find_all() when you meant to call find()?" % key
#AttributeError: ResultSet object has no attribute 'text'. You're probably treating a list of items like a single item. Did you call find_all() when you meant to call find()?
    return None

search = raw_input("enter search string")#input
search_google(search)#searching str
#working fine
