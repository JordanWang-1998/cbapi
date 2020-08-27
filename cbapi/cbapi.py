'''
    a full-featured API library to allow downloading and presenting organization and people data from Crunchbase
'''

import pandas as pd
import json
import requests
import threading

RAPIDAPI_KEY  = "4166b8c4fcmsh77ea0f96ec19fe0p14a98ajsn8b6e21c88565"


def trigger_api_orgs(page = "", since_time = "", name="", query="", domain = "", locations="", types=""):
    '''trigger Crunchbase API for orgaization data of certain pages'''

    querystring = {
        "page": page,                   # query specific pages, if not specified then query all pages
        "updated_since": since_time,    # query data that is updated since "updated_since" timestamp
        "name": name,                   # full-text search of organization name, aliases
        "query": query,                 # full-text search of organization name, aliases, short description
		"domain_name": domain,			# full-text search of organization domain_name, e.g. "www.amazon.com"
        "locations": locations,         # filter by locations, e.g. "China,Beijing"
		"organization_types": types		# filter by organization types, e.g. "company", "investor", "school", "group"
    }

    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_orgs = pd.DataFrame(json.loads(response.text))                  # response in dataframe, using json.loads()
    
    return response_orgs


def threader_orgs(result_list, page = "", since_time = "", name="", query="", domain = "", locations="", types=""):
    '''threader function to trigger Crunchbase API for organization data of certain pages'''
    response_orgs = trigger_api_orgs(page, since_time, name, query, domain, locations, types)
    result_list.append(pd.DataFrame(list(pd.DataFrame(response_orgs["data"]["items"])["properties"])))
	
	
def get_orgs(page = "", since_time = "", name="", query="", domain = "", locations="", types=""):
    '''trigger Crunchbase API for organization data of all pages'''

    response_orgs = trigger_api_orgs(page, since_time, name, query, domain, locations, types)
	
    if page != "":
        result = pd.DataFrame(list(pd.DataFrame(response_orgs["data"]["items"])["properties"]))      # dataframe of organization data of certain pages
        
    else:
        num_pages = response_orgs['data']['paging']['number_of_pages'] 		# number of pages
        print("number of pages: ", num_pages)
        threads = [None for _ in range(num_pages)]                          # list of threads
        result_list = []                                                    # list of organization data of each page in dataframe
        
        for i in range(num_pages):
            threads[i] = threading.Thread(target = threader_orgs, args = (result_list, str(i+1), since_time, name, query, domain, locations, types))
            threads[i].start()                                              		# start all threads
        
        for i in range(num_pages):
            threads[i].join()                                               		# join all threads
        
        result = pd.concat(result_list, axis = 0)       # dataframe of organization data of all pages
    
    # set index to "name"
    result.set_index(result["name"], inplace=True)
    return result


def trigger_api_ppl(page = "", since_time = "", name="", query="", locations="", socials="", types=""):
    '''trigger Crunchbase API for people data of certain pages'''

    querystring = {
        "page": page,                   # query specific pages, if not specified then query all pages
        "updated_since": since_time,    # query data that is updated since "updated_since" timestamp
        "name": name,                   # full-text search of name only
        "query": query,                 # full-text search of name, title, company
        "locations": locations,         # filter by locations, e.g. "China,Beijing"
        "socials": socials,             # filter by social media identity, e.g. "ronconway"
        "types": types                  # filter by type, e.g. "investor"
    }

    headers = {
        'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
    }

    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_ppl = pd.DataFrame(json.loads(response.text))                  # response in dataframe, using json.loads()

    return response_ppl


def threader_ppl(result_list, page = "", since_time = "", name="", query="", locations="", socials="", types=""):
    '''threader function to trigger Crunchbase API for people data of certain pages'''
    response_ppl = trigger_api_ppl(page, since_time, name, query, locations, socials, types)
    result_list.append(pd.DataFrame(list(pd.DataFrame(response_ppl["data"]["items"])["properties"])))


def get_ppl(page="", since_time = "", name="", query="", locations="", socials="", types=""):
    '''trigger Crunchbase API for people data of all pages'''

    response_ppl = trigger_api_ppl(page, since_time, name, query, locations, socials, types)
    
    if page != "":
        result = pd.DataFrame(list(pd.DataFrame(response_ppl["data"]["items"])["properties"]))      # dataframe of people data of certain pages
        
    else:
        num_pages = response_ppl['data']['paging']['number_of_pages']       # number of pages
        print("number of pages: ", num_pages)
        threads = [None for _ in range(num_pages)]                          # list of threads
        result_list = []                                                    # list of people data of each page in dataframe
        
        for i in range(num_pages):
            threads[i] = threading.Thread(target = threader_ppl, args = (result_list, str(i+1), since_time, name, query, locations, socials, types))
            threads[i].start()                                              # start all threads
        
        for i in range(num_pages):
            threads[i].join()                                               # join all threads
            
        result = pd.concat(result_list, axis = 0)       # dataframe of people data of all pages
    
    # set index to "first_name last_name"
    result.set_index(result["first_name"] + " " + result["last_name"], inplace=True)
    return result


