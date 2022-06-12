from typing import List 
import yake


def extract_keywords(text, n = 3) -> List[tuple[str, float]]:
    kw_extractor = yake.KeywordExtractor(top=n, stopwords=None, n=1)
    keywords = kw_extractor.extract_keywords(text.lower())
    return list(map(lambda x: (x[0], -x[1]), keywords))

# print("TextRank")
# start = time.time()
# TR_keywords = summa_keywords.keywords(full_text, scores=True)
# for kw, v in TR_keywords[0:5]:
#   print("Keyphrase: ", kw, ": score", v)
# print("took:", time.time() - start)

# print("---------------------\n")

if __name__ == "__main__":
    text = "Praga Praga Praga Praga Praga xxx"
    
    print(extract_keywords(text))