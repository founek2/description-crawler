from gensim.test.utils import common_texts
from gensim.models import Word2Vec
import gensim.downloader

# print(common_texts)
# model = Word2Vec(sentences=common_texts, vector_size=100, window=5, min_count=1, workers=4)
# model.save("word2vec.model")

# model = gensim.downloader.load('word2vec-google-news-300')
model = gensim.downloader.load('glove-wiki-gigaword-100')
# Word2Vec.load()
print("locality", model.similarity("prague", "locality"))
print("political", model.similarity("prague", "political"))
# print("liquor_store", model.similarity("prague", "liquor store"))