from transformers import pipeline

'''
[{'entity': 'NC', 'score': 0.7792173624038696, 'word': '[CLS]'},
 {'entity': 'DP', 'score': 0.9996283650398254, 'word': 'Mis'},
 {'entity': 'NC', 'score': 0.9999253749847412, 'word': 'amigos'},
 {'entity': 'VMI', 'score': 0.9998560547828674, 'word': 'están'},
 {'entity': 'VMG', 'score': 0.9992249011993408, 'word': 'pensando'},
 {'entity': 'SP', 'score': 0.9999602437019348, 'word': 'en'},
 {'entity': 'VMN', 'score': 0.9998666048049927, 'word': 'viajar'},
 {'entity': 'SP', 'score': 0.9999545216560364, 'word': 'a'},
 {'entity': 'VMN', 'score': 0.8722310662269592, 'word': 'Londres'},
 {'entity': 'DD', 'score': 0.9995203614234924, 'word': 'este'},
 {'entity': 'NC', 'score': 0.9999248385429382, 'word': 'verano'},
 {'entity': 'NC', 'score': 0.8802427649497986, 'word': '[SEP]'}]
'''

class PosTaggerService:

    def __init__(self, device_index = 0):
        self.tagger = pipeline(
            "ner",
            model="mrm8488/bert-spanish-cased-finetuned-pos",
            tokenizer=(
                'mrm8488/bert-spanish-cased-finetuned-pos',
                {"use_fast": False}
            ),
            device=device_index
            )

    def tag(self, sentence, target_word):
        # Use the word in the pipeline to tokenized it and grab the first token.
        # We want to check POS on the context provided by the sentence, not here.
        tokenized_word = self.tagger(target_word)
        if len(tokenized_word) == 0:
            return ''

        token = tokenized_word[0]['word']

        res = self.tagger(sentence)
        result = next( item for item in res if item['word'] == token)
        return result['entity']