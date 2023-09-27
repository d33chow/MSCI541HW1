import sys
import csv
import os

if len(sys.argv) >= 4:
    folderPath = sys.argv[1]
    refType = sys.argv[2]
    ref = sys.argv[3]
else:
    print('Insufficient parameters provided')
    print('Please provide a folder directory, "id" or "docno", and an ID or Doc No.')
    print('Stopping...')
    sys.exit()

# folderPath = 'outPath'
# refType = 'docno'
# ref = 'LA010189-0018'

# refType = 'id'
# ref = 6832

isDoc = False
if refType == 'docno':
    subfolder = ref[2:8]
    docno = ref

    # I stole csv reading code from here https://stackoverflow.com/questions/26082360/python-searching-csv-and-return-entire-row
    csv_file = csv.reader(open('meta.csv', "r"), delimiter=",")
    for row in csv_file:
        if ref == row[1]:
            isDoc = True
            id = row[0]
            headline = row[2]
            date = subfolder[:2] + "/" + subfolder[2:4] + "/" + subfolder[4:6]
elif refType == 'id':
    id = ref
    csv_file = csv.reader(open('meta.csv', "r"), delimiter=",")
    for row in csv_file:
        if str(ref) == row[0]:
            isDoc = True
            docno = row[1]
            subfolder = docno[2:8]
            headline = row[2]
            date = subfolder[:2] + "/" + subfolder[2:4] + "/" + subfolder[4:6]
else:
    print("Invalid reference type")
    print("Please enter the decompressed folder directory, 'id' or 'docno', then a file ID or Doc No.")
    print("Stopping...")
    sys.exit()

if not isDoc:
    print("Invalid reference")
    print("Please enter a valid ID or doc no.")
    print("Stopping...")
    sys.exit()

print("Doc No.: " + docno)
print("Internal ID: " + str(id))
print("Headline: " + headline)
print("Date published: " + date)

# Folder directory management (and other instances of it in this file) come from this link
# https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
parent = os.getcwd()
if not os.path.isdir(folderPath):
    print('Folder name not found in folder')
    print('Please provide a subfolder that exists as the first parameter')
    print('If the parameters are still not working, try using the relative directory paths')
    print('Stopping...')
    sys.exit()

directory = os.path.join(parent, folderPath)
directory = os.path.join(directory, subfolder)
directory = os.path.join(directory, docno + ".txt")

with open(directory, 'r') as doc:
    print("Document content:")
    for line in doc:
        print(line)