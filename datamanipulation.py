import re
import json
from nltk.corpus import stopwords
from nltk import bigrams
from collections import Counter
import string

tweet = []
tweet_count = 0

# reading the tweets
with open('tweetdata.jsonl', 'r') as f:
    # converting the JSON data into a python dictionary
    for line in f:
        try:
            tweet.append(json.loads(line))
            # print(json.dumps(tweet, indent=4))
        except BaseException as e:
            pass
# Tokenization starts here

# The tokenisation is based on regular expressions (regexp)
# A general-purpose English tokeniser like the one from NLTK, does not capture peculiarities like
# @-mentions, emoticons, URLs and #hash-tags are not recognised as single tokens
# The following code proposes a pre-processing chain that will consider these aspects of the language
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


with open('tweetdata.jsonl', 'r') as f:
    for line in f:
        # print(word_tokenize(tweet[tweet_count]['text']))
        tokens = preprocess(tweet[0]['text'])
        tweet_count += 1

# Now we have fairly meaningful data to work with

fname = 'tweetdata.jsonl'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        try:
            tweets = json.loads(line)
        except BaseException as e:
            pass

        # Create a list with all the terms
        terms_all = [term for term in preprocess(tweets['text'])]

        # Removing stop words, punctuations and unnecessary characters
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['RT', 'via', '️', '…']
        # add characters in above list if needed
        terms_filtered = [term for term in preprocess(tweets['text']) if term not in stop]

        # Count terms only once
        terms_single = set(terms_all)

        # Count hashtags only
        terms_hash = [term for term in preprocess(tweets['text'])if term.startswith('#')]

        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweets['text']) if term not in stop and not term.startswith(('#', '@'))]

        # More often than not simple term frequencies don’t give us a deep explanation of what the text is about.
        # To put things in context, let’s consider sequences of two terms (a.k.a. bigrams).
        terms_bigram = bigrams(terms_filtered)

        # Update the counter
        count_all.update(terms_only) # change the type of term here if need be

    # Print the first n most frequent words
    print("NO. OF MOST FREQUENT WORDS YOU WANT TO ACCESS? >>>>>")
    n = int(input())
    print(count_all.most_common(n))
