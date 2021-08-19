from nltk import wordnet as wn

# Or, equivalently
nouns = set()
for sentence in my_corpus.sents():
# each sentence is either a list of words or a list of (word, POS tag) tuples
for word, pos in nltk.pos_tag(sentence): # remove the call to nltk.pos_tag if `sentence` is a list of tuples as described above

if pos in ["NN", "NNP"]: # feel free to add any other noun tags
nouns.add(word)