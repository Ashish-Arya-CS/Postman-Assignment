#Importing necessary Libraries
import requests
import pandas as pd
import math
from ratelimit import limits, sleep_and_retry
import pyodbc

#Change the username, password and server address
username = 'Sa' 
password = 'Mssql123' 
server = 'localhost'

#Handling rate-limit
# 5 calls per minute
CALLS = 5
RATE_LIMIT = 60

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
#Empty function just to check for calls to API
    return

#Function to get token whenever required
def getToken():
    check_limit()
    r = requests.get('https://public-apis-api.herokuapp.com/api/v1/auth/token')
    response = r.json()
    myToken = response['token']
    return myToken

#Function to get all the categories from the public api and returning it in a dataframe
def getCategories(myToken):
    check_limit()
    URL = 'https://public-apis-api.herokuapp.com/api/v1/apis/categories?page={}'.format(1)
    head = {'Authorization': 'token {}'.format(myToken)}
    response = (requests.get(URL, headers=head)).json()
    if('error' in response.keys()):
        head = {'Authorization': 'token {}'.format(getToken())}
        response = (requests.get(URL, headers=head)).json()    
    count = response['count']
    pages = math.ceil(count/10)
    df = pd.DataFrame(columns=['categories'])
    for i in response['categories']:
        df = df.append({'categories': i}, ignore_index=True)    
    if(pages>1):
        j = 2
        while(j <= pages):
            URL = 'https://public-apis-api.herokuapp.com/api/v1/apis/categories?page={}'.format(j)
            response = (requests.get(URL, headers=head)).json()
            if('error' in response.keys()):
                head = {'Authorization': 'token {}'.format(getToken())}
                response = (requests.get(URL, headers=head)).json()
            
            for i in response['categories']:
                df = df.append({'categories': i}, ignore_index=True)
            j = j+1        
    return df                    

#Calling the function getCategories and storing the categories in a dataframe
categories_df = getCategories(getToken())

#Crawling through all the APIs and storing the data in a dataframe
URL = 'https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={pageN}&category={categoryN}'.format(pageN=1, categoryN=(categories_df['categories'][0]))
head = {'Authorization': 'token {}'.format(getToken())}
response = (requests.get(URL, headers=head)).json()
data = pd.DataFrame(columns=['API', 'Description', 'Auth', 'HTTPS', 'Cors', 'Link', 'Category'])
for counter in range(len(response['categories'])):
    temp = pd.Series(response['categories'][counter], index = data.columns)
    data = data.append(temp, ignore_index=True)
    
for i in range(len(categories_df['categories'])):
    check_limit()
    print('Extracting data from category - {}'.format(categories_df['categories'][i]))
    pageNumber = 1
    if(i==0):
        pageNumber = pageNumber + 1
        URL = 'https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={pageN}&category={categoryN}'.format(pageN=pageNumber, categoryN=(categories_df['categories'][i]))
        response = (requests.get(URL, headers=head)).json()
        for counter in range(len(response['categories'])):
            temp = pd.Series(response['categories'][counter], index = data.columns)
            data = data.append(temp, ignore_index=True)
    else:    
        URL = 'https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={pageN}&category={categoryN}'.format(pageN=pageNumber, categoryN=(categories_df['categories'][i]))
        response = (requests.get(URL, headers=head)).json()
        if('error' in response.keys()):
            head = {'Authorization': 'token {}'.format(getToken())}
            response = (requests.get(URL, headers=head)).json()
        for counter in range(len(response['categories'])):
            temp = pd.Series(response['categories'][counter], index = data.columns)
            data = data.append(temp, ignore_index=True)
        pageNumber = pageNumber + 1
        count = response['count']
        pages = math.ceil(count/10)
        while(pageNumber <= pages):
            check_limit()
            URL = 'https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={pageN}&category={categoryN}'.format(pageN=pageNumber, categoryN=(categories_df['categories'][i]))
            response = (requests.get(URL, headers=head)).json()
            if('error' in response.keys()):
                head = {'Authorization': 'token {}'.format(getToken())}
                response = (requests.get(URL, headers=head)).json()    
            for counter in range(len(response['categories'])):
                temp = pd.Series(response['categories'][counter], index = data.columns)
                data = data.append(temp, ignore_index=True)
            pageNumber = pageNumber + 1        

 
database = 'TestDB'  
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Insert Dataframe into SQL Server:
for index, row in data.iterrows():
    cursor.execute("INSERT INTO dbo.Assignment (API ,Description ,Auth ,HTTPS ,Cors ,Link, Category) values(?,?,?,?,?,?,?)", row.API, row.Description, row.Auth, row.HTTPS, row.Cors, row.Link, row.Category)
cnxn.commit()
cursor.close()