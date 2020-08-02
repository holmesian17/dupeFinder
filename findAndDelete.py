from PIL import Image
from difflib import SequenceMatcher
import imagehash
import os
import glob
import sys
import textdistance

#images need to be in the order they were scanned

directory = 'images'

hashes = {}

def getImageHashes():
    # status bar variables
    numberOfFiles = len(glob.glob1(directory,"*.tif"))
    statusNumber = 0
    # iterate over files
    for file in os.listdir(directory):
        # only tif files
        if file.endswith(".tif"):
            # to access the file, it needs directory structure in front
            imgfile = os.path.join(directory, file)
            # creates the image hash of the imagefile - 16 bit hash
            hash = imagehash.phash(Image.open(imgfile), 16)
            # turns the hash into a string
            hash = str(hash)
            # adds the file name to the hash in the dictionary
            hashes[file] = hash
            #bumps the status up and creates a rough percent of it
            statusNumber += 1
            status = round((statusNumber/numberOfFiles)*100)
            # needs to be sys.write so that it doesn't just print a long list
            print('Working:',status,'%')
        else:
            continue

    # print(hashes)

def checkImageHashes():
    # gets the keys and values from the hashes dictionary, in order
    items = sorted(hashes.items())
    # print("Results:") - this is for checking the images
    # iterates over the current and next tuple in the directory
    for cur, nxt in zip(items, items[1:]):

        text1 = cur[1] # gets the 2nd item in the tuple, the image file itself
        text2 = nxt[1] # gets the 2nd item in the tuple, the image file itself
        # finds the variation in the image hashes using the Levenshtein algorithm
        answer = textdistance.hamming(text1, text2)

        # if the Levenshtein difference between the 32 character strings is less than
        # 30, it detects the image as a duplicate and deletes the current image,
        # keeping the subsequent image
        if 0 <= answer <= 30:
            toDelete = os.path.join(directory, cur[0])
            # this moves them to the recyle bin
            os.remove(toDelete)

# do we want this file to log which files were deleted in a text file in the folder
# and then delete itself?

'''
# this is for testing and showing the similarity of the images, over one 1000 image folder
# it had a 100% success rate with no false duplicates

        if 10 <= answer <= 30:
            print("Similar:       ", cur[0], nxt[0], "Deviations:", answer)
        elif 1 <= answer <= 10:
            print("Highly likely: ", cur[0], nxt[0], "Deviations:", answer)
        elif 0 == answer:
            print("Duplicate:     ", cur[0], nxt[0], "Deviations:", answer)
        else:
            #print("No Match: ", answer, cur[0], nxt[0])
            continue
'''
#to print answers and hashes: answer, cur[0], nxt[0], cur[1], nxt[1]
# if 0 to 30, we can go ahead and delete all the cur[0]s, the final nxt[0] is the
# keeper



getImageHashes()
checkImageHashes()

## DONE!
## run hashes for all of the images in the folder
## add hashes to list
## if hashes similar within one or two characters, highlight? print? delete?
## doesn't need to run a similarity calculation against every string, just the
## one next to it as that's where dupes would be
## test accuracy of this to see potential - try different hashing algs, longer hashes
## for better results???
