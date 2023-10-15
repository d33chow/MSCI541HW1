import sys
import csv
import os
import numpy as np
import string
import nltk
from nltk.tokenize import word_tokenize
from collections import deque

# if len(sys.argv) >= 4:
#     folderPath = sys.argv[1]
#     qFile = sys.argv[2]
#     output = sys.argv[3]
# else:
#     print('Insufficient parameters provided')
#     print('Please provide a folder directory, "id" or "docno", and an ID or Doc No.')
#     print('Stopping...')
#     sys.exit()

# if qFile[-4:] != ".txt":
#     print('Invalid query file provided')
#     print('Please provide a .txt file for the query')
#     print('Stopping...')
#     sys.exit()

# queryD = os.path.join(folderPath, qFile)
# queries = []
# with open(directory, 'r') as doc:
#     TopNum = None
#     for line in doc:
#         if TopNum == None:
#             TopNum = int(line)
#         else:
#             queries.append([TopNum, line])
#             TopNum = None

queries = [["1", "Big Win"]]
with open('lexicon.npy', 'rb') as f:
    lexicon = np.load(f).tolist()
print(lexicon)
with open('inverted-index.npy', 'rb') as f:
    invIndex = np.load(f).tolist()
for query in queries:
    qTerms = word_tokenize(query[1])
    # Line below taken from https://bobbyhadz.com/blog/python-remove-punctuation-from-list
    qTerms = [item.translate(string.punctuation).lower() for item in qTerms]
    qTermsTF = [invIndex.index(item) for item in qTerms]

    qTF = deque(qTermsTF)
    while len(qTF) > 1:
        tf1 = qTF.popleft()
        tf2 = qTF.popleft()

        tfFinal = [item[0](tf2.count(item[0]) > 0) for item in tf1]
        qTF.append(tfFinal)
    else:
        tfFinal = qTf.pop()

    print(tfFinal)






