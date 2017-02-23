import csv
import requests
import json
import time
import sys

###### EDIT INPUT PARAMETERS START ##########
campaign_name = '<CAMPAIGN_NAME>'
account_id = '<ACCOUNT_ID>' # Your ad account id withou act_
token = '<ACCESS_TOKEN>'
promoted_page_id = '<PAGE_ID>'
adset_budget = 'BUDGET_IN_CENTS' # this is in cents, default is $5000
###### EDIT INPUT PARAMETERS STOP ##########

###### Optional parameters to be edited start
campaign_objective = "LINK_CLICKS"
adset_end_time = str(int(time.time())+2330000) # this is in unix time default is current time + 1 month
adset_name = 'DCO Ad Set'
###### Optional parameters to be edited stop

adset_end_time = str(int(time.time())+2330000) # this is in unix time default is current time + 1 month
adset_name = 'DCO Ad Set'

if(len(sys.argv) < 3):
    print "Please provide a file with dco images, bodies titles etc. python dco.py -f dco_input.csv"
    sys.exit(0)

file_path = sys.argv[2] # file path to sample file with images,bodies,titles, descriptions and links


def create_campaign():
    files = {
        'name': campaign_name,
        'objective': campaign_objective,
        'status': 'PAUSED',
        'access_token': token
    }
    headers = {'Content-Type': 'application/json'}
    url = 'https://graph.facebook.com/v2.8/act_' + account_id + '/campaigns'
    r = requests.post(url, data=json.dumps(files), headers=headers)
    if ('error' in r.json()):
        print "ERROR IN CAMPAIGN CREATION: "
        print r.json()
        return None
    else:
        return r.json()['id']

def dataToVal(data, iden, key ):
    values = data[iden]
    result = []
    for value in values:
        result.append({key: value})
    return result

def create_asset_feed(token, data):
    images = dataToVal(data, 'images', 'url')
    bodies = dataToVal(data, 'bodies', 'text')
    titles = dataToVal(data, 'titles', 'text')
    desc = dataToVal(data, 'descriptions', 'text')
    urls = dataToVal(data, 'links', 'website_url')
    files = {
        'images': images,
        'bodies': bodies,
        'titles': titles,
        'descriptions': desc,
        'ad_formats': ['SINGLE_IMAGE'],
        'link_urls': urls,
        'access_token': token,
    }
    headers = {'Content-Type': 'application/json'}
    url = 'https://graph.facebook.com/v2.8/act_' + account_id + '/adasset_feeds'
    r = requests.post(url, data=json.dumps(files), headers=headers)
    if ('error' in r.json()):
        print "ERROR IN FEED CREATION: "
        print r.json()
        return None
    else:
        return r.json()['id']

def create_adset(token, campaign_id, feed_id):
    ad_set_files = {
        'name': adset_name,
        'asset_feed_id': feed_id,
        'campaign_id': campaign_id,
        'optimization_goal': 'LINK_CLICKS',
        'billing_event': 'IMPRESSIONS',
        'is_autobid': 'true',
        'promoted_object': {'page_id': promoted_page_id},
        'lifetime_budget': adset_budget,
        'end_time': adset_end_time,
        'targeting': {
         'geo_locations':{'countries':['US']},
         'publisher_platforms':['facebook']
         },
        'access_token': token
    }
    headers = {'Content-Type': 'application/json'}
    url = 'https://graph.facebook.com/v2.8/act_' + account_id + '/adsets'
    r = requests.post(url, data=json.dumps(ad_set_files), headers=headers)
    return r.json()

def parse(file_name, feed_data):
    with open(file_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            iden = row[0]
            for i in range(1, len(row)):
                feed_data[iden].append(row[i])
    return feed_data

feed_data = {
    'images' : [],
    'bodies' : [],
    'links' : [],
    'titles' : [],
    'descriptions' : [],
    'links' : []
}

campaign_id = create_campaign()
if(campaign_id):
    print "Campaign created with id: ", str(campaign_id)
    data = parse(file_path,feed_data)
    feed_id = create_asset_feed(token, data)
    if(feed_id):
        print "DCO Feed created, id: " + str(feed_id)
        r = create_adset(token, campaign_id, feed_id)
        if ('error' in r):
            print "ERROR IN AD SET CREATION: "
            print r
        else:
            print "DCO Adset created, PAUSED by default, adset id: ",r['id']
            print "Visit this link or your ads manager to review and activate your ad campaign"
            print "https://www.facebook.com/ads/manager/account/adsets/?act="+ account_id+"&selected_campaign_ids="+campaign_id
