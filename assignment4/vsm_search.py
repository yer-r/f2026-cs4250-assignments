#-------------------------------------------------------------------------
# AUTHOR: Eric Kim
# FILENAME: vsm_search.py
# SPECIFICATION: Vector Space Model search engine. Documents and queries are
#                represented with TF-IDF (stopwords removed, nothing else),
#                documents are ranked per query by cosine similarity, and
#                Average Precision (AP) per query and Mean Average Precision
#                (MAP) are computed from the relevance judgments.
# FOR: CS 5180- Assignment #3
# TIME SPENT: around 3 hours total
#-----------------------------------------------------------*/

# importing required libraries
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------
# 1. Load the input files
# ---------------------------------------------------------
docs = pd.read_csv("docs.csv")
queries = pd.read_csv("queries.csv")
judgments = pd.read_csv("relevance_judgments.csv")

doc_ids = docs["doc_id"].tolist()

# ---------------------------------------------------------
# 2. Build the TF-IDF matrix for the documents
# ---------------------------------------------------------
# Requirement: remove stopwords only
vectorizer = TfidfVectorizer(stop_words="english")
doc_matrix = vectorizer.fit_transform(docs["text"])

# ---------------------------------------------------------
# 3. Process each query and compute AP values
# ---------------------------------------------------------
ap_scores = {}

for _, row in queries.iterrows():
    query_id = row["query_id"]

    # Representing the query in the same TF-IDF space as the documents
    query_vector = vectorizer.transform([row["query_text"]])

    # Scoring every document with cosine similarity
    scores = cosine_similarity(query_vector, doc_matrix).flatten()

    # Ranking all documents from highest to lowest score (stable for ties)
    ranking = np.argsort(-scores, kind="stable")
    ranked_doc_ids = [doc_ids[i] for i in ranking]

    # Retrieving the relevant documents for this query
    relevant = set(
        judgments[(judgments["query_id"] == query_id) &
                  (judgments["judgment"] == "R")]["doc_id"]
    )

    # -----------------------------------------------------
    # 4. Compute Average Precision (AP)
    # -----------------------------------------------------
    hits = 0
    precision_sum = 0.0
    for rank, doc_id in enumerate(ranked_doc_ids, start=1):
        if doc_id in relevant:
            hits += 1
            precision_sum += hits / rank

    # store the AP value for this query (use any data structure you prefer)
    ap_scores[query_id] = precision_sum / len(relevant) if relevant else 0.0

# ---------------------------------------------------------
# 5. Sort queries by AP in descending order
# ---------------------------------------------------------
sorted_queries = sorted(ap_scores.items(), key=lambda item: item[1], reverse=True)

# ---------------------------------------------------------
# 6. Print the sorted queries and their AP scores
# ---------------------------------------------------------
print("====================================================")
print("Queries sorted by Average Precision (AP):")
for query_id, ap in sorted_queries:
    print(f"{query_id}: AP = {ap:.4f}")

# Mean Average Precision across all queries
map_score = sum(ap_scores.values()) / len(ap_scores)
print("----------------------------------------------------")
print(f"MAP = {map_score:.4f}")
