# Postman Data Engineer Intern Assignment
## Public APIs List Crawler

### Problem Statement
We need to crawl the list of all APIs from the Public APIs github repo (https://github.com/public-apis/public-apis) and store it in a database.

### Points to achieve
- Your code should follow concept of OOPS
- Support for handling authentication requirements & token expiration of server
- Support for pagination to get all data
- Develop work around for rate limited server
- Crawled all API entries for all categories and stored it in a database

### Steps to Execute
Assuming SQL server 2016 or above and Python 3.x version has been installed on client machine.
Run the below commands in appropriate terminal/command prompt

1) pip install -r /path/to/requirements.txt
2) sqlcmd -S myServer\instanceName -i prescript.sql
3) Please change the username, password and server address on line number 9,10,11 in code.py
4) python3 code.py

### Table  and DB Details
Database Name - TestDB
Schema Name - dbo
Table Name - Assignment
Total Columns - 7
Column Names - API ,Description ,Auth ,HTTPS ,Cors ,Link, Category

### Achieved points from Points to achieve


✅ Your code should follow concept of OOPS - I have made use of funcions in my code which makes it modular and lays emphasis on code reusability.<br>
✅ Support for handling authentication requirements & token expiration of server - I have handled the authentication requirements & token expiration by keeping a check on the response of the API and if the token expires, then I make a request for a new token.<br>
✅ Support for pagination to get all data - I have added support for pagination in my code. I am calculating the total number of pages through the count that I am getting as a part of reponse from the server. Once I get the total number of pages, I am keeping a track of the current page Number in my code.<br>
✅ Develop work around for rate limited server - Since the server supports only 10 requests per minute. I have handled this case by making use ratelimit library from python which keeps a track of requests made while running my code and if it exceeds the set limit then the code is put on hold for 1 minute and then again the requests are made.<br>
✅ Crawled all API entries for all categories and stored it in a database - I have crawled all the API entries of all the categories and stored the data in a database.<br>

### The total number of entries in my table is 525 which can be verified from the jupiter notebook.

### Not done from Points to achieve 
None, I have completed all the points to achieve.

### Further Improvements
- In my code I have set the rate limit to 5 while using the ratelimt library but since this library does not keep a track of all the API calls made on a global level so keeping the rate limit to maximum which is 10 tends to throw an error. So, I kept the rate limit to 5 in my case which takes a little more time to extract all the data but it does deliver the result. If there had been more time I would have tried to handle the rate limit situation more efficiently.
