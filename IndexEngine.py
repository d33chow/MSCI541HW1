# Used link to find how to have command-line parameters
# https://moez-62905.medium.com/the-ultimate-guide-to-command-line-arguments-in-python-scripts-61c49c90e0b3 
import sys
import os
import time
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
import numpy as np
import re
lexicon = deque()
invIndex = deque()
wordCount = []

import string

# def tokenize(q: deque(), id: int):
#     wordQ = deque()
#     while len(q) != 0:
#         qString = q.popleft()
#         # Find the start of the three sections terms are collected from
#         if qString[:6] == "<TEXT>" or qString[:9] == "<GRAPHIC>" or qString[:10] == "<HEADLINE>":
#             # All sections end with this
#             while qString[:2] != "</" or qString[:3] == "</P" :
#                 qString = q.popleft()
#                 if qString[:1] != "<":
#                     tokens = word_tokenize(qString)
#                     # qString below taken from https://bobbyhadz.com/blog/python-remove-punctuation-from-list
#                     tokens = [item.translate(string.punctuation).lower() for item in tokens]
#                     wordQ.extend(tokens)
    
#     # print(wordQ)
#     docCount = len(wordQ)
#     wordCount.append(docCount)

#     c = 0
#     tf = []
#     while c < docCount:
#         curTF = [wordQ[c], wordQ.count(wordQ[c])]
#         if tf.count(curTF) <= 0 or len(tf) <= 0:
#             tf.append(curTF)
#         c = c + 1

#     # print(tf)
#     for cTF in tf:
#         if lexicon.count(cTF[0]) == 0 or len(lexicon) == 0:
#             lexicon.append(cTF[0])
#             invIndex.append([])
#         termID = lexicon.index(cTF[0])
#         invIndex[termID].append([id, cTF[1]])

    # print(invIndex)


try:
    with gzip.open(inPath,'rt') as f:
        q = deque()
        wordQ = deque()
        toCount = False
        for line in f:
            # queue information from 
            # https://www.geeksforgeeks.org/queue-in-python/
            q.append(line)
            if line[:7] == "<DOCNO>":
                docname = line[8:len(line)-10]+".txt"
                date = line[10:16]
            elif line[:10] == "<HEADLINE>" or buffer == 1:
                buffer = buffer + 1
            elif buffer == 2:
                headline = line[:len(line)-1]
                buffer = 0
            elif line[:6] == "</DOC>":
                # txt file writing from https://www.pythontutorial.net/python-basics/python-write-text-file/
                directory = os.path.join(outPath, date)
                # tokenize(q.copy(), id)
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

                # The rest of this if-statement is from the function
                wordCount.append(len(wordQ))

                # no duplicate list from https://www.w3schools.com/python/python_howto_remove_duplicates.asp
                noDupes = list(dict.fromkeys(wordQ))
                lexicon.extend(noDupes)
                lexicon = list(dict.fromkeys(lexicon))
                # idea of extending list with empty arrays comes from https://stackoverflow.com/questions/10712002/create-an-empty-list-with-certain-size-in-python
                invIndex.extend([[]] * (len(lexicon) - len(invIndex)))
                for word in noDupes:
                    invIndex[lexicon.index(word)].append((id, wordQ.count(word)))
                wordQ.clear()
                print(id)

            # if-statement adapted from function
            if toCount and line[:1] != "<":
                # Line below taken from https://bobbyhadz.com/blog/python-remove-punctuation-from-list
                wordQ.extend([re.sub(r'[^\w\s]','',item) for item in line.lower().split()])
            elif line[:4] == "<TEX" or line[:4] == "<GRA" or line[:4] == "<HEA":
                toCount = True
            elif line[:3] == "</T" or line[:3] == "</G" or line[:3] == "</H":
                toCount = False

            

    # used numpy to save indexes using info from https://numpy.org/doc/stable/reference/generated/numpy.save.html
    with open('lexicon.npy', 'wb') as f:
        np.save(f, np.array(*lexicon))
    with open('inverted-index.npy', 'wb') as f:
        np.save(f, np.array(*invIndex))
    with open('doc-length.npy', 'wb') as f:
        np.save(f, np.array(*wordCount))

# Found exception from https://docs.python.org/3/library/gzip.html
except (OSError, gzip.BadGzipFile):
    print('Invalid text document provided')
    print('Please provide a .gz file as the first parameter')
    print('Stopping...')
    sys.exit()