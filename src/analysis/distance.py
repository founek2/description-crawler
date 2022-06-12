import threading
import time
from typing import List
import gensim.downloader
import Levenshtein 

# def begin_load_model():
#     global import_thread
#     import_thread = threading.Thread(target=load_model_thread)
#     import_thread.start()

# def load_model_thread():
#     global model
#     print("start loading")
#     model = gensim.downloader.load('glove-wiki-gigaword-100')
#     print("done importing")

# def wait_load():
#     print('wait')
#     import_thread.join()
#     print('done')

# def do_other_things():
#     time.sleep(1)

# begin_load_model()
# wait_foo()

print("loading model")
# model = gensim.downloader.load('glove-wiki-gigaword-100')
model = {}
print("loaded")

def fallback_distance(keyword: str, kw: str) -> tuple[float, str]:
    return Levenshtein.jaro_winkler(keyword, kw), "jaro_winkler"

# word2vec 0.4 minimal
# jaro_winkler 0.6
def calc_distances(keyword: str, keywords: List[str]):
    keyword = keyword.lower()
    # if import_thread.is_alive():
    #     wait_load()
    print("calc", keyword, keywords)
    distances = []
    for kw in keywords:
        if kw in model and keyword in model:
            result = float(model.similarity(keyword, kw)), "word2vec"
        else:
            result = fallback_distance(keyword, kw)
        distances.append(result)
    print("distances", distances)

    return distances
    