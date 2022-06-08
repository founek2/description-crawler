import time 
import yake
from summa import keywords as summa_keywords
from keybert import KeyBERT
import Levenshtein 

def calc_distance(kw: str):
  return Levenshtein.distance(kw.lower(), "locality"), Levenshtein.jaro_winkler(kw.lower(), "locality")

full_text = """
Prague is the capital and largest city in the Czech Republic, and the historical capital of Bohemia. On the Vltava river, Prague is home to about 1.3 million people. The city has a temperate oceanic climate, with relatively warm summers and chilly winters.
Prague is a political, cultural, and economic hub of central Europe, with a rich history and Romanesque, Gothic, Renaissance and Baroque architecture. It was the capital of the Kingdom of Bohemia and residence of several Holy Roman Emperors, most notably Charles IV (r. 1346–1378). It was an important city to the Habsburg monarchy and Austro-Hungarian Empire. The city played major roles in the Bohemian and the Protestant Reformations, the Thirty Years' War and in 20th-century history as the capital of Czechoslovakia between the World Wars and the post-war Communist era.
Prague is home to a number of well-known cultural attractions, many of which survived the violence and destruction of 20th-century Europe. Main attractions include Prague Castle, Charles Bridge, Old Town Square with the Prague astronomical clock, the Jewish Quarter, Petřín hill and Vyšehrad. Since 1992, the historic center of Prague has been included in the UNESCO list of World Heritage Sites.
"""

print("YAKE")
kw_extractor = yake.KeywordExtractor(top=10, stopwords=None)

start = time.time()
keywords = kw_extractor.extract_keywords(full_text.lower())
for kw, v in keywords:
  print("Keyphrase: ", kw, ": score", v, calc_distance(kw))
  
print("took:", time.time() - start)

print("---------------------\n")

print("TextRank")
start = time.time()
TR_keywords = summa_keywords.keywords(full_text, scores=True)
for kw, v in TR_keywords[0:10]:
  print("Keyphrase: ", kw, ": score", v)
print("took:", time.time() - start)

print("---------------------\n")


# print("KeyBERT")
# kw_model = KeyBERT(model='all-mpnet-base-v2')

# start = time.time()
# keywords = kw_model.extract_keywords(full_text, 
#                                      keyphrase_ngram_range=(1, 2), 
#                                      stop_words='english', 
#                                      highlight=False,
#                                      top_n=10
#                                      )

# for kw, v in keywords[0:10]:
#   print("Keyphrase: ", kw, ": score", v)
# print("took:", time.time() - start)

# print("---------------------\n")

# vzít top 10, spočítat vzdálenosti proti types a zobrazit výsledky