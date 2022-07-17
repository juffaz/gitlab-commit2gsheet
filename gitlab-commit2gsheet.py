import requests
import pandas as pd
#import matplotlib.pyplot as plt
import openpyxl
import gspread
from datetime import datetime, timedelta
import datetime as dt
import os
from oauth2client.service_account import ServiceAccountCredentials


WORKSHEET_KEY = os.environ.get('WORKSHEET_KEY',)
GITLAB_GROUPS = os.environ.get('GITLAB_GROUPS')
GITLAB_GROUPS = [int(s) for s in GITLAB_GROUPS.split(',')]
print(GITLAB_GROUPS)
print(type(GITLAB_GROUPS))
PRIVATE_TOKEN = os.environ.get('PRIVATE_TOKEN', )
GITLAB_DOMAIN = os.environ.get('GITLAB_DOMAIN', )
GITLAB_API_URL_GROUP_ONE = "https://" + GITLAB_DOMAIN + "/api/v4/groups/"
GITLAB_API_URL_GROUP_TWO = "/projects?include_subgroups=yes"
GITLAB_API_URL_COMMIT_ONE = "https://" + GITLAB_DOMAIN + "/api/v4/projects/"


def gitlab_commit_date(day_minus):
    return (datetime.today() - timedelta(days=day_minus)).strftime("%Y-%m-%d")

gitlab_date = gitlab_commit_date(100)

GITLAB_API_URL_COMMIT_SINCE = "?ref=main&since="
GITLAB_API_URL_COMMIT_DATE =  GITLAB_API_URL_COMMIT_SINCE + str(gitlab_date)
GITLAB_API_URL_COMMIT_MIX =  "/repository/commits" + GITLAB_API_URL_COMMIT_DATE + "&page=1&per_page=200"
GITLAB_API_URL_COMMIT_TWO = GITLAB_API_URL_COMMIT_MIX  ##"/repository/commits"  # ?since=2016-07-31&page=1&per_page=2
print(GITLAB_API_URL_COMMIT_TWO)

def get_data(url):
    response = requests.get(url, headers={"PRIVATE-TOKEN":PRIVATE_TOKEN}, verify=True)
    data = response.json()
    print(url)
    return data



def get_project_url_in_group(GITLAB_GROUPS): 
    project_urls = []
    #project_names = []
    for i in GITLAB_GROUPS: 
       base_url = GITLAB_API_URL_GROUP_ONE   
       full_url = base_url + str(i) + GITLAB_API_URL_GROUP_TWO
       data = get_data(full_url)
       data = project_urls.append(data)
    return project_urls

def get_id_in_group():
    project_url_in_group = get_project_url_in_group(GITLAB_GROUPS)
    ids = {}
    pnames = []
    for d in project_url_in_group:
          for dic1 in d:
                 ids[dic1['id']] = dic1['name']
    return(ids)




def get_commits(project_ids):
    pass
    projects_commits = []
    project_name = []
    number = 0
    for index, (key, value) in enumerate(project_ids.items()):
        base_url = GITLAB_API_URL_COMMIT_ONE
        full_url = base_url + str(key) + GITLAB_API_URL_COMMIT_TWO
        data = get_data(full_url)
        projects_commits.append(data)
        for i in range(len(projects_commits[number])):
            projects_commits[number][i]['project_name'] = value
        number +=1
    return projects_commits

def get_commits_fields():
    get_id = get_id_in_group()          
    get_commits_info = get_commits(get_id)
    get_commit_infos = get_commits_info
    author_name = []
    author_email = []
    message = []
    committed_date = []
    web_url = []
    pname = []

    for i in get_commit_infos:
        #print(i)
        for info in i:
               author_name.append(info['author_name'])
               author_email.append(info['author_email'])
               message.append(info['message'])
               committed_date.append(info['committed_date'])
               web_url.append(info['web_url'])
               pname.append(info['project_name'])

    return author_name, author_email, message, committed_date, web_url, pname

def data2pandas(commit_day):
    global df
    gitlab_date = gitlab_commit_date(commit_day)
    global GITLAB_API_URL_COMMIT_DATE
    GITLAB_API_URL_COMMIT_DATE =  GITLAB_API_URL_COMMIT_SINCE + str(gitlab_date)
    data_commits = get_commits_fields()
    df = pd.DataFrame({'ProjectName': data_commits[5], 'Name' : data_commits[0], 'Message' : data_commits[1], 'Author_email' : data_commits[2], 'Committed_date' : data_commits[3], 'web_url' : data_commits[4]})

testik = 10




def pandas2xlsx(comm_day):
    data2pandas(comm_day)
    df.to_excel(r'dataframe.xlsx', index = False, header=True)   

#pandas2xlsx()

print(GITLAB_API_URL_COMMIT_TWO)

def pandas2gsheets():

     scope = [
     'https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'
     ]
     creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
     client = gspread.authorize(creds)
     #sh = client.create('micro2022br')
     sh = client.open_by_key(WORKSHEET_KEY)
     worksheet = sh.get_worksheet(0)
     worksheet.format("A1:F1", {
               "backgroundColor": {
                 "red": 0,
                 "green": 128,
                 "blue": 0
               },
               "horizontalAlignment": "CENTER",
               "textFormat": {
                 "fontSize": 12,
                 "bold": True
               }
     })
     worksheet.update([df.columns.values.tolist()] + df.values.tolist())

#pandas2gsheets()

def main():
    pandas2xlsx(testik)
    pandas2gsheets()

if __name__ == "__main__":
    main() 
