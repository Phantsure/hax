import os, slackclient, time
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import requests

# delay in seconds before checking for new events
SOCKET_DELAY = 1
# slackbot environment variables
my_api_key = os.environ.get('my_api_key')
my_cse_id = os.environ.get('my_cse_id')
SLACK_NAME = os.environ.get('SLACK_NAME')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_ID = os.environ.get('SLACK_ID')
slack_client = slackclient.SlackClient(SLACK_TOKEN)


def is_for_me(event):
    return event.get('user') == SLACK_ID




def post_message(message, channel):
    slack_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)

def run():
    if slack_client.rtm_connect():
        print('[.] Valet de Machin is ON...')
        while True:
            event_list = slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if is_for_me(event):
                        results = google_search(event.get('text'), my_api_key, my_cse_id, num=10)
                        handle_message(search_term=results[0].get('link'),channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')




def scrape(url):
    url_obj_data  = requests.get(url)
    url_text_data = url_obj_data.text
    soup = BeautifulSoup(url_text_data,'html.parser')
    answer_element = soup.find("div", { "class" : "accepted-answer" })
    # print answer_element.prettify()
    pre = answer_element.findAll("pre")
    return pre


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def handle_message(url,channel):
    code = scrape(url)
    for x in code:
        reply = "```%s```" % (x.text)
        post_message(message=reply, channel=channel)


if __name__=='__main__':
    run()
