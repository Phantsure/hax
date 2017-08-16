from bs4 import BeautifulSoup
import requests
import webbrowser


def scrape(url):
    url_obj_data  = requests.get(url)
    url_text_data = url_obj_data.text
    soup = BeautifulSoup(url_text_data,'html.parser')
    answer_element = soup.find("div", { "class" : "accepted-answer" })
    # print answer_element.prettify()
    pre = answer_element.findAll("pre")
    for x in pre:
        print (x.text)
    return None

def search_google():
	url_list = []
	search_string=  input("enter search string : ")
	#search_string = 'cats'
	#search_result = google.search(search_string+' in python -url"stack oveflow"',1)
	search_result = requests.get('https://www.google.com/search?q=' + search_string)
	#print(search_result.text)
	

	soup = BeautifulSoup(search_result.text,"lxml")
	#print(soup.prettify())
	for anchor in soup.findAll('a', href=True):
		x = 0
		anchor = str(anchor)
		#print(anchor,'\n')
		while x<14:
			if anchor[x] == '<a href="/url?'[x]:
				r = True
			else:
				r = False
			x = x+1
		if r==True:
			url = anchor
			break

	link_soup = BeautifulSoup(url,'lxml')
	tag = link_soup.a
	tag.name = 'a'
	url = 'www.google.com'+tag['href']
	scrape(url)
	print(url)
	#webbrowser.open(url)
	  
search_google()
