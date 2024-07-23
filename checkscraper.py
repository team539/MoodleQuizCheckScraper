import sys
from bs4 import BeautifulSoup
import csv
import re

html_content = sys.stdin.read()

writer = csv.writer(sys.stdout)

soup = BeautifulSoup(html_content, 'html.parser')
print(soup.title.text)

tables = soup.find_all('table',class_='generaltable')

table = tables[0]
row = table.find('tr')
cols = row.find_all('td')  # Use 'th' if you want to extract headers
#cols = [ele.text.strip() for ele in cols]
print(cols[0].text)
anchor=cols[0].find('a')
url=anchor.get('href')
# print(url)
match=re.search(r'\?id=(\d+)\&',url)
if match:
    uid=match.group(1)
    print(uid)

table = tables[1]
if True:
    rows = table.find_all('tr')
    data = []

    for row in rows:
        cols = row.find_all('td')  # Use 'th' if you want to extract headers
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    
    for row in data:
#        print(row)
        writer.writerow(row)
    
#    <div role="main"><table class="generaltable generalbox quizreviewsummary">