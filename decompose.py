import sys
import csv
import re
import argparse
#import ansconfig

import sys
import signal

# Ignore SIGPIPE and don't throw exceptions on it
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-nh","--noheading",action="store_true")
    parser.add_argument("-q","--questionid", type=int, help="Specify the question ID as an integer")
    args=parser.parse_args()

    table=[]
    anslist=[]
    prtlist=[]
    prtgradelist=[]
    top=True
    
    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    questionidpos=8
    submissionpos=11
    for row in reader:
        if top:
            head=row
            submissionpos=head.index('submission')
            questionidpos=head.index('questionid')     
            top=False
            continue
        
        submission=row[submissionpos]
        
        if args.questionid is not None and args.questionid!=int(row[questionidpos]):
            continue
        
        pattern = r'(ans\d+): ([^;]+) \[score\]'
        matches = re.findall(pattern, submission)
        
        anss={}
        for tup in matches:
            if tup[0] not in anslist:
                anslist.append(tup[0])
            
            if tup[0] not in anss.keys():
                anss[tup[0]]=tup[1]
            else:
                anss[tup[0]]=anss[tup[0]]+'; '+tup[1]
        row.append(anss)
        ansspos=-3
                
        pattern = r'(prt\d+)-(\d+-[TF])'
        matches = re.findall(pattern, submission) # from submission

        prts={}
        for tup in matches:
            if tup[0] not in prtlist:
                prtlist.append(tup[0])
            
            if tup[0] not in prts.keys():
                prts[tup[0]]=tup[1]
            else:
                prts[tup[0]]=prts[tup[0]]+'; '+tup[1]
        row.append(prts)
        prtspos=-2
        
        pattern = r'(prt\d+): ([^|;]*)([!|;]|$)'
        matches = re.findall(pattern, submission) # from submission

        prtgrades={}
        for tup in matches:
            if (tup[0]+'grade') not in prtgradelist:
                prtgradelist.append(tup[0]+'grade')
            
            if tup[0] not in prtgrades.keys():
                prtgrades[tup[0]+'grade']=tup[1]
            else:
                prtgrades[tup[0]+'grade']=prtgrades[tup[0]]+'; '+tup[1] # not happening
        row.append(prtgrades)
        prtgradespos=-1
                
        table.append(row)

    if not args.noheading:
        writer.writerow(head+anslist+prtlist+prtgradelist)

    for row in table:
        record=row[0:ansspos]
        
        for ans in anslist:
            if ans in row[ansspos].keys():
                record.append(row[ansspos][ans])
            else:
                record.append('')
        for prt in prtlist:
            if prt in row[prtspos].keys():
                record.append(row[prtspos][prt])
            else:
                record.append('')
        for prtgrade in prtgradelist:
            if prtgrade in row[prtgradespos].keys():
                record.append(row[prtgradespos][prtgrade])
            else:
                record.append('')
        
        writer.writerow(record)
        
if __name__ == "__main__":
    main()