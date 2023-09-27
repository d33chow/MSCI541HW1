# Used link to find how to have command-line parameters
# https://moez-62905.medium.com/the-ultimate-guide-to-command-line-arguments-in-python-scripts-61c49c90e0b3 
import sys
import os
if len(sys.argv) < 3:
  print('Insufficient parameters provided')
  print('Please provide a document directory, new folder name')
  print('Stopping...')
  sys.exit()
else:
    inPath = sys.argv[1]
    outPath = sys.argv[2]
# inPath = 'latimes.gz'
# outPath = 'outPath'

# Folder directory management (and other instances of it in this file) come from this link
# https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
parent = os.getcwd()
outPath = os.path.join(parent, outPath)
if os.path.isdir(outPath):
    print('Folder name found in folder')
    print('Please provide a compressed document file name, new folder name')
    print('If the parameters are still not working, try using the relative directory paths')
    print('Stopping...')
    sys.exit()
else:
    os.mkdir(outPath)

# Used link for code below
# https://stackoverflow.com/questions/10566558/read-lines-from-compressed-text-files
import gzip
from collections import deque
import csv

id = 1
buffer = 0

try:
    with gzip.open(inPath,'rt') as f:
        q = deque()
        for line in f:
            # queue information from 
            # https://www.geeksforgeeks.org/queue-in-python/
            

            q.append(line)
            if line[:6] != "</DOC>":
                if line[:7] == "<DOCNO>":
                    docname = line[8:len(line)-10]+".txt"
                    date = line[10:16]
                elif line[:10] == "<HEADLINE>" or buffer == 1:
                    buffer = buffer + 1
                elif buffer == 2:
                    headline = line[:len(line)-1]
                    buffer = 0
            else:
                # txt file writing from https://www.pythontutorial.net/python-basics/python-write-text-file/
                directory = os.path.join(outPath, date)
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                fileDirectory = os.path.join(directory, docname)
                with open(fileDirectory, 'w') as doc:
                    doc.write(q.popleft())
                with open(fileDirectory, 'a') as doc:
                    while len(q) != 0:
                        doc.write(q.popleft())

                # I stole code from this https://docs.python.org/3/library/csv.html
                if id == 1:
                    with open('meta.csv', 'w', newline='') as csvfile:
                        headers = ['ID', 'Doc No.', 'Headline', 'Date']
                        metadata = csv.DictWriter(csvfile, fieldnames=headers)
                        metadata.writerow({'ID': id, 'Doc No.': docname[:len(docname)-4], 'Headline': headline, 'Date': date})
                        id = id + 1
                else:
                    with open('meta.csv', 'a', newline='') as csvfile:
                        headers = ['ID', 'Doc No.', 'Headline', 'Date']
                        metadata = csv.DictWriter(csvfile, fieldnames=headers)
                        metadata.writerow({'ID': id, 'Doc No.': docname[:len(docname)-4], 'Headline': headline, 'Date': date})
                        id = id + 1
# Found exception from https://docs.python.org/3/library/gzip.html
except (OSError, gzip.BadGzipFile):
    print('Invalid text document provided')
    print('Please provide a .gz file as the first parameter')
    print('Stopping...')
    sys.exit()
