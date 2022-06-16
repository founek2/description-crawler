# description-crawler

## word2vec

[https://github.com/RaRe-Technologies/gensim-data](https://github.com/RaRe-Technologies/gensim-data)

## Posibilities

-   trip advisor reviews -> API
-   search first wiki by name - for long addresses google is not working
    -   maybe could just improve google query???
-   crawl for images - og:image
-   Wikipedia - compare coordinates with googleID

<!-- -   https://wikitravel.org - load time > 20s :( -->

## Env

-   `API_CRAWL_STREAM_PATH` - default `/crawl-stream`
-   `API_CRAWL_PATH` - default `/crawl`

## API

-   `/crawl?id=INTERNAL_ID` - classic REST API, returns {data, links, place}
-   `/crawl-stream?id=INTERNAL_ID` - chunked REST API, first chunk is {links, place}, then data element per chunk. Each chunk is separeted by `///\n`

> INTERNAL_ID is stellar id of place

example response:

```json
{
    "data": [
        {
            "heading": "Grand Rapids, Michigan",
            "paragraphs": [
                "Grand Rapids is a city and county seat of Kent County in the U.S. state of Michigan.  At the 2020 census, the city had a population of 198,917 which ranks it as the second most-populated city in the state after Detroit.  Grand Rapids is the central city of the Grand Rapids metropolitan area, which has a population of 1,087,592 and a combined statistical area population of 1,383,918.\n",
                "Situated along the Grand River approximately 25 mileseast of Lake Michigan, it is the economic and cultural hub of West Michigan, as well as one of the fastest-growing cities in the Midwest.[6]  A historic furniture manufacturing center, Grand Rapids is home to five of the world's leading office furniture companies and is nicknamed \"Furniture City.\" Other nicknames include \"River City\" and more recently, \"Beer City\". The city and surrounding communities are economically diverse, based in the health care, information technology, automotive, aviation, and consumer goods manufacturing industries, among others.\n"
            ],
            "link": "https://en.wikipedia.org/wiki/Grand_Rapids,_Michigan",
            "keywords": [
                {
                    "kw": "city",
                    "score": -0.04151012223926566,
                    "distance": {
                        "score": 0.4754253625869751,
                        "alg": "word2vec"
                    }
                },
                {
                    "kw": "grand",
                    "score": -0.04759813757461727,
                    "distance": {
                        "score": 1.0,
                        "alg": "word2vec"
                    }
                },
                {
                    "kw": "rapids",
                    "score": -0.05946067052001552,
                    "distance": {
                        "score": 0.3244970738887787,
                        "alg": "word2vec"
                    }
                }
            ]
        },
        {
            "heading": "Home ",
            "paragraphs": ["The official website of the City of Grand Rapids."],
            "link": "https://www.grandrapidsmi.gov/Home",
            "keywords": [
                {
                    "kw": "rapids",
                    "score": -0.09568045026443411,
                    "distance": {
                        "score": 0.3244970738887787,
                        "alg": "word2vec"
                    }
                },
                {
                    "kw": "official",
                    "score": -0.15831692877998726,
                    "distance": {
                        "score": 0.4056321382522583,
                        "alg": "word2vec"
                    }
                },
                {
                    "kw": "website",
                    "score": -0.15831692877998726,
                    "distance": {
                        "score": 0.20040081441402435,
                        "alg": "word2vec"
                    }
                }
            ]
        }
    ],
    "links": [
        "https://en.wikipedia.org/wiki/Grand_Rapids,_Michigan",
        "https://cs.wikipedia.org/wiki/Grand_Rapids_(Michigan)",
        "https://www.grandrapidsmi.gov/Home"
    ],
    "place": {
        "id": "3e5fa772-b720-4a89-9aac-a4c9149bca7c",
        "data": {
            "address": "Grand Rapids, MI, USA",
            "phone_number": null,
            "international_phone_number": null,
            "name": "Grand Rapids",
            "website_url": "http://www.grcity.us/",
            "types": [
                {
                    "id": "locality",
                    "display_name": "locality"
                },
                {
                    "id": "political",
                    "display_name": "political"
                }
            ],
            "coordinates": {
                "lat": 42.9633599,
                "lon": -85.6680863
            },
            "viewport": {
                "northeast": {
                    "lat": 43.02905094827491,
                    "lon": -85.5686459371687
                },
                "southwest": {
                    "lat": 42.88366594045422,
                    "lon": -85.75153207124804
                }
            },
            "rating": 0,
            "reviews": [],
            "opening_hours": null
        }
    }
}
```
