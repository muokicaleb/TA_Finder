import os
import traceback
from sentence_transformers import SentenceTransformer, util
import numpy as np
from ast import literal_eval

embedder = SentenceTransformer(os.getenv('TRANSFORMER_MODEL'))
corpus = literal_eval(os.getenv('TWITTER_TOPICS'))

corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

top_k = 3

def query_similar(query):

    query_embedding = embedder.encode(query ,convert_to_tensor=True)
    print("embedded")
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu()
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 3 most similar sentences in corpus:")

    similar_categories = []
    for idx in top_results[0:top_k]:
        print(corpus[idx].strip(), "(Score: %.4f)" % (cos_scores[idx]))
        similar_categories.append(corpus[idx].strip())
    return similar_categories

def multiple_query_similar(queries):
    final_similar_results = []
    for query in queries:
        try:
            query_embedding = embedder.encode(query, convert_to_tensor=True)
            cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
            cos_scores = cos_scores.cpu()

            #We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

            print("\n\n======================\n\n")
            print("Query:", query)
            print("\nTop 5 most similar sentences in corpus:")

            similar_categories = []
            for idx in top_results[0:top_k]:
                print(corpus[idx].strip(), "(Score: %.4f)" % (cos_scores[idx]))
                similar_categories.append(corpus[idx].strip())
            final_similar_results = final_similar_results + similar_categories
        except:
            similar_categories = []
            final_similar_results = final_similar_results + similar_categories


    return final_similar_results
