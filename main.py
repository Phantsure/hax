import slackclient, time
from bs4 import BeautifulSoup
import requests
import string

# delay in seconds before checking for new events
SOCKET_DELAY = 1
# slackbot environment variables

search_url="default"
VALET_SLACK_TOKEN='YOUR API KEY'
VALET_SLACK_NAME="YOUR BOT NAME"
VALET_SLACK_ID='BOT ID'
valet_slack_client = slackclient.SlackClient(VALET_SLACK_TOKEN)


def handle_message(message, user, channel):
    search_string = message + ' python -url"stack overflow"'
    #search_string.replace("<@U6PNMBJMC>","")
    search_string = remove_all("<@U6PNMBJMC>",search_string)
    #print search_string
    url = search_google(search_string)
    #print "got url %s" % url
    code = scrape(url)
    if code !=None:
        for x in code:
            reply = "```%s```" % (x.text)
            post_message(message=reply, channel=channel)
    else:
        post_message(message="ERROR",channel=channel)

def post_message(message, channel):
    valet_slack_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)

def run():
    if valet_slack_client.rtm_connect():
        print('[.] Slacker is ON...')
        while True:
            event_list = valet_slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    if event.get('type') == 'message':
                        reply = event.get('text')
                        if reply == None:
                            reply="none"
                        #print reply
                        #print event.get('channel')
                        if (("<@U6PNMBJMC>" in reply) or (event.get('channel') == "D6NPML7S7")) and (event.get('user') != VALET_SLACK_ID)  :
                            handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')


# def search_google(search_string):
#     search_result = google.search('%s in python -url"stack oveflow"' %(search_string),1)
#     url = search_result[0].link
#     return url

def search_google(search):
	url_list = []
	search_result = requests.get('https://www.google.com/search?q=' + search)
	soup = BeautifulSoup(search_result.text,"html.parser")
	for anchor in soup.findAll('a', href=True):
		x = 0
		anchor = str(anchor)
		while x<14:
			if anchor[x] == '<a href="/url?'[x]:
				r = True
			else:
				r = False
			x = x+1
		if r==True:
			search_url = anchor
			break
	link_soup = BeautifulSoup(search_url,'html.parser')
	tag = link_soup.a
	tag.name = 'a'
	url = 'https://'+'www.google.com'+tag['href']
	return url

def scrape(url):
    #print "scraping"
    url_obj_data  = requests.get(url)
    url_text_data = url_obj_data.text
    soup = BeautifulSoup(url_text_data,'html.parser')
    answer_element = soup.find("div", { "class" : "accepted-answer" })
    if answer_element == None:
        return None
    # print answer_element.prettify()
    pre = answer_element.findAll("pre")
    return pre

def remove_all(substr, str):
    index = 0
    length = len(substr)
    while string.find(str, substr) != -1:
        index = string.find(str, substr)
        str = str[0:index] + str[index+length:]
    return str

if __name__=='__main__':
    run()
