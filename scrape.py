import sys
from bs4 import BeautifulSoup
import csv
import re
import argparse
#import ansconfig

import sys
import signal

class ansconfig:
    anshead=[]
    prthead=[]

# Ignore SIGPIPE and don't throw exceptions on it
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def main():
    html_content = sys.stdin.read()
    writer = csv.writer(sys.stdout)

    parser=argparse.ArgumentParser()
    parser.add_argument("-nh","--noheading",action="store_true")
    args=parser.parse_args()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    title=soup.h1.text

    reviewtable = soup.find('table',class_=['generaltable','quizreviewsummary'])

    row = reviewtable.find('tr')
    cols = row.find_all('td')  # Use 'th' if you want to extract headers

    userdisplayname=cols[0].text
    anchor=cols[0].find('a')
    url=anchor.get('href')

    match=re.search(r'\?id=(\d+)\&',url)
    if match:
        uid=match.group(1)

#    attemptid = soup.find('input', {'name': 'pageurl'})['value'].split('attempt=')[1].split('&')[0]
    link=soup.find('a', href=lambda x: x and '/mod/quiz/reviewquestion.php' in x)
    if link:
        attemptid=link['href'].split('attempt=')[1].split('&')[0]
    else:
        attemptid=0

    link=soup.find('a', href=lambda x: x and '/mod/quiz/review.php' in x)
    if link:
        cmid=link['href'].split('cmid=')[1].split('&')[0]
    else:
        cmid=0
        
    links = soup.find_all('a', href=lambda x: x and '/question/type/stack/questiontestrun.php' in x)
    qids=[link['href'].split('questionid=')[1].split('&')[0] for link in links]
#    for link in links:
#    if link:
#        qid = link['href'].split('questionid=')[1].split('&')[0]
#    else:
#        qid = 0
        
    breadcrumb = soup.find(id='page-navbar')
    cname = breadcrumb.find('a').text.replace(" ", "").replace("\n", "").replace("\t", "")
    cid = breadcrumb.find('a')['href'].split('id=')[1]

    questionid=0
    fixed=[cid,cname,cmid,title,attemptid,uid,userdisplayname]
    head=['cid','cname','cmid','qname','attemptid','uid','uname','qid','questionid','stepid','date','submission','status','grade']
    
    if not args.noheading:
        writer.writerow(head+ansconfig.anshead+ansconfig.prthead)
    
    tables = soup.find_all('table',class_='generaltable')
    
    for table in tables:
        if 'quizreviewsummary' not in table.get('class'):
            questionid+=1 # should be retrieved from q55257:2_ans etc.
            rows = table.find_all('tr')
            data = []
        
            for row in rows:
                record = row.find_all('td')  # Use 'th' if you want to extract headers
                record = [ele.text.strip() for ele in record]
                if record:
                    submission=record[2].replace("\"\"","EMPTYSTRING") # bs4 interpretes &quot;&quot; as ""
                    record[2]=submission
                    
                    pattern = r'(ans\d+): ([^;]+) \[score\]' # to be strict, pattern should be read from ansconfig.anshead
                    matches = re.findall(pattern, submission) 

                    anslist=[]
                    for ans in ansconfig.anshead:
                        result = next((tup[1] for tup in matches if tup[0] == ans),"")
                        anslist.append(result)

                    
                    pattern = r'(prt\d+)-(\d+-[TF])'
                    matches = re.findall(pattern, submission) # from submission

                    prtlist=[]
                    for prt in ansconfig.prthead:
                        result = [tup[1] for tup in matches if tup[0] == prt]
                        prtlist.append(', '.join(map(str, result)))
                    
                    qid=0
                    if len(qids)>=questionid:
                        qid=qids[questionid-1]                        
                    
                    data.append(fixed+[qid,questionid]+record+anslist+prtlist)

            for row in data:
                writer.writerow(row)
        
#    <div role="main"><table class="generaltable generalbox quizreviewsummary">

if __name__ == "__main__":
    main()