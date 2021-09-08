import nltk
from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt

# B

from nltk import download
from nltk.corpus import brown
from nltk.corpus import gutenberg
from nltk.corpus import cess_esp
#from unigram import UnigramModel

# improts
from src.FileHelper import write_txt

# A
def run_a():
	nltk.download('cess_esp')
	nltk.download('averaged_perceptron_tagger')

	# Read the corpus into a list,
	# each entry in the list is one sentence.
	cess_sents = cess.tagged_sents()

	# Train the unigram tagger
	uni_tag = ut(cess_sents)

	sentence = "guapa"

	# Tagger reads a list of tokens.
	uni_tag.tag(sentence.split(" "))

	# Split corpus into training and testing set.
	train = int(len(cess_sents)*90/100) # 90%

	# Train a bigram tagger with only training data.
	bi_tag = bt(cess_sents[:train])

	# Evaluates on testing data remaining 10%
	bi_tag.evaluate(cess_sents[train+1:])

	# Using the tagger.
	bi_tag.tag(sentence.split(" "))

	res = nltk.pos_tag("ella es guapa".split(" "))
	print(res)

# https://github.com/zelliott/maple/blob/11cfe6889e22e89715f91270bd854762574a8cd6/models/build_models.py
# https://sites.google.com/view/programacion-en-python/home/5-etiquetado-morfosint%C3%A1tico
# list(filter(len, [word + "=> " + tag if "a" in tag else "" for (word,tag) in cess_esp.tagged_words()]))
# len(list(filter(len, [word + "=> " + tag if tag.startswith("a") else "" for (word,tag) in cess_esp.tagged_words()])))
# 13703
# len(list(filter(len, [word + "=> " + tag if tag.startswith("aq") else "" for (word,tag) in cess_esp.tagged_words()])))
# 12976
# len(list(filter(len, [word + "=> " + tag if tag.startswith("ao") else "" for (word,tag) in cess_esp.tagged_words()])))
# 727
def build_spanish():
	download('cess_esp')
	words = cess_esp.words()

	total_size = len(words)
	print('Spanish Corpus contains ' + str(total_size) + ' total tokens')

	esp_trainfiles = [' '.join(words)]
	#return UnigramModel(esp_trainfiles)

# build_spanish()

def generar_fichero(items):

	# minus
	items = [item.lower() for item in items]

	# sin duplicados
	items = list(dict.fromkeys(items))

	items.sort()

	return "\n".join(items)

def extraer_adjetivos():
	download('cess_esp')
	words = cess_esp.words()
	adjetivos_tagged = list(filter(len, [word + "\t" + tag if tag.startswith("a") else "" for (word,tag) in cess_esp.tagged_words()]))
	adjetivos = list(filter(len, [word if tag.startswith("a") else "" for (word,tag) in cess_esp.tagged_words()]))

	write_txt(generar_fichero(adjetivos), "../../TextTools/GenerarListadoPalabras/result/adjetivos.txt")
	write_txt(generar_fichero(adjetivos_tagged), "../../TextTools/GenerarListadoPalabras/result/adjetivos_tagged.txt")

def extraer_nacionalidades():
	download('cess_esp')
	nacionalidades_m_ruido_tagged = list(filter(len, [word + "\t" + tag if tag.startswith("aq0ms0") else "" for (word,tag) in cess_esp.tagged_words()]))
	nacionalidades_m_ruido = list(filter(len, [word if tag.startswith("aq0ms0") else "" for (word,tag) in cess_esp.tagged_words()]))
	write_txt(generar_fichero(nacionalidades_m_ruido), "../../TextTools/GenerarListadoPalabras/result/nacionalidades_ruido_aq0ms0.txt")
	write_txt(generar_fichero(nacionalidades_m_ruido_tagged), "../../TextTools/GenerarListadoPalabras/result/nacionalidades_ruido_aq0ms0_tagged.txt")


#extraer_nacionalidades()
extraer_adjetivos()