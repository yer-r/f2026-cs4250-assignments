#-------------------------------------------------------------------------
# AUTHOR: Eric Kim
# FILENAME: index.py
# SPECIFICATION: This is for Question 8 of Assignment 1, where we have to create a Python program that would solve Question 7. 
# FOR: CS 4250 - Assignment #1
# TIME SPENT: around 27 minutes
#-------------------------------------------------------------------------
# Importing Python libraries
import pandas as pd

# Reading the document collection
data = pd.read_csv("collection.csv")

# Defining the dictionary used for lemmatization
# --> add your Python code here
lemmas = {
  "new": "new",
  "homes": "home",
  "home": "home",
  "increases": "increase",
  "increasing": "increase",
  "sale": "sale",
  "sales": "sale",
  "rising": "rise",
  "rise": "rise",
  "in": "in",
  "july": "july"
}
# Creating the data structure that will store the inverted index
invertedIndex = {}


# Processing each document in the collection
for i, row in data.iterrows():
docID = row["Document"]
text = row["Text"]
# Applying surface-level normalization
# use lower() to normalize lowercase in Python, replace(".", "") to get rid of periods
text = text.lower()
text = text.replace(".", "")

# Tokenizing the document
# use split() to turn the text into a list of strings
tokenList = text.split()

# Applying lemmatization
newTokens = []

for token in tokenList:
    if token in lemmas:
        newTokens.append(lemmas[token])
    else:
        newTokens.append(token)

tokenList = newTokens


# Building the inverted index

for term in tokenList:
    if term not in invertedIndex:
        invertedIndex[term] = []
    if docID not in invertedIndex[term]:
        invertedIndex[term].append(docID)

# Printing the inverted index with terms ordered alphabetically
# Expected format:
# term1 : ['Doc1', 'Doc2']
# term2 : ['Doc3']
for term in sorted(invertedIndex):
    print(term, ":", invertedIndex[term])
