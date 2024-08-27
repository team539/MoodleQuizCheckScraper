import sys
from bs4 import BeautifulSoup
import csv
import re
import argparse

def main():
    html_content = sys.stdin.read()
    writer = csv.writer(sys.stdout)

    parser=argparse.ArgumentParser()
    parser.add_argument("-nh","--noheading",action="store_true")
    args=parser.parse_args()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    title=soup.h1.text

    tables = soup.find_all('table',class_='generaltable')

    table = tables[0]
    row = table.find('tr')
    cols = row.find_all('td')  # Use 'th' if you want to extract headers

    userdisplayname=cols[0].text
    anchor=cols[0].find('a')
    url=anchor.get('href')

    match=re.search(r'\?id=(\d+)\&',url)
    if match:
        uid=match.group(1)

    attemptid = soup.find('input', {'name': 'pageurl'})['value'].split('attempt=')[1].split('&')[0]
    cmid = soup.find('input', {'name': 'pageurl'})['value'].split('cmid=')[1]


    link = soup.find('a', href=lambda x: x and '/question/type/stack/questiontestrun.php' in x)

    if link:
        qid = link['href'].split('questionid=')[1].split('&')[0]

    breadcrumb = soup.find(id='page-navbar')
    cname = breadcrumb.find('a').text
    cid = breadcrumb.find('a')['href'].split('id=')[1]

    fixed=[cid,cname,qid,title,attemptid,uid,userdisplayname]
    head=['cid','cname','qid','qname','attemptid','uid','uname','checkid','date','submission','status','grade']
    
    table = tables[1]
    if True:
        rows = table.find_all('tr')
        data = []

    
        for row in rows:
            record = row.find_all('td')  # Use 'th' if you want to extract headers
            record = [ele.text.strip() for ele in record]
            if record:
                data.append(fixed+record)

            #TODO: decompse ansn etc
            
        if not args.noheading:
            writer.writerow(head)

        for row in data:
            writer.writerow(row)
        
#    <div role="main"><table class="generaltable generalbox quizreviewsummary">

if __name__ == "__main__":
    main()
