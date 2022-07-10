# Based on
# https://medium.com/bukalapak-data/inferring-causality-from-observational-data-hands-on-introduction-32b06fff59a1

# Dado un template
# y un listado de pares de palabras malas
# Comparar si cambiar el genero es confundidor

# imports
from transformers import AutoTokenizer, AutoModelForMaskedLM, FillMaskPipeline
from scipy.stats import t
import numpy as np

# Datos
sentence_before = "El nuevo vendedor de la compañía es <mask>."
sentence_after = "La nueva vendedora de la compañía es <mask>."
sentence_after = "El nuevo vendedor de la compañía es <mask>."
sentence_before = "La nueva vendedora de la compañía es <mask>."

confounder = "genre"

treated_expected_insultos = ["imbécil", "gilipollas", "idiota"]
treated_expected_calificativos = ["inútil", "torpe", "incompetente"]

# Config
tokenizername = modelname = "PlanTL-GOB-ES/roberta-base-bne"
modelsize = 50262 # Fuente => El depurador#30522 # https://github.com/google-research/bert/issues/149

# Init model
tokenizer = AutoTokenizer.from_pretrained(tokenizername)
model = AutoModelForMaskedLM.from_pretrained(modelname).to('cuda')
model.eval()

pipeline = FillMaskPipeline(model, tokenizer, top_k=modelsize, device=model.device.index)

# helpers
def tokenize_as_ids(word):
    return tokenizer.convert_tokens_to_ids(tokenizer.tokenize(word))

def find_suggestion_by_id(suggestion_list, token_id):
    return next(filter(lambda suggestion: suggestion["token"] == token_id, suggestion_list))

def find_suggestion(suggestion_list, word):
    res = []
    token_ids = tokenize_as_ids(word)
    for token_id in token_ids:
        entry = find_suggestion_by_id(suggestion_list, token_id)
        res.append(entry)
    return res

# formulas
def att_estimator(y_i_list: list[float], y_ji_list: list[float]):
    l = [x - y for x, y in zip(y_i_list, y_ji_list)]
    l2 = [x**2 for x in l]

    return np.mean(l2)

# if and only if there are any untreated members that are being used more than once as a match to the treated, otherwise we only use the first term.
def att_estimator_variance(y_i_list: list[float], y_ji_list: list[float], att_estimator_result: float):
    l = [x - y - att_estimator_result for x, y in zip(y_i_list, y_ji_list)]
    return np.mean(l)

# app
suggestions_before = pipeline(sentence_before)
suggestions_after = pipeline(sentence_after)

score_before_list = []
score_after_list = []

for insulto in treated_expected_insultos:
    suggestion_before = find_suggestion(suggestions_before, insulto)
    suggestion_after = find_suggestion(suggestions_after, insulto)

    # En los multitoken nos quedamos con el primero, más significado?
    score_before = suggestion_before[0]["score"]
    score_after = suggestions_after[0]["score"]

    score_before_list.append(score_before)
    score_after_list.append(score_after)

att_estimation = att_estimator(score_before_list, score_after_list)
att_estimation_var = att_estimator_variance(score_before_list, score_after_list, att_estimation)

if att_estimation_var < 0:
    att_estimation_var = att_estimation_var*-1

conf = t.ppf(0.025, att_estimation_var)

lb = att_estimation + conf
ub = att_estimation - conf

print("att_estimation " + str(att_estimation))
print("att_estimation_var " + str(att_estimation_var))
print("conf " + str(conf))

print("The estimated ATT is {} IDR".format(att_estimation))
print("The 95% confidence interval is between {0} and {1}".format(lb, ub))

x = 0

# Normal

# att_estimation 0.000542357169921755
# att_estimation_var -0.02383092019462385
# conf -3.061417881763607e+53
# The estimated ATT is 0.000542357169921755 IDR
# The 95% confidence interval is between -3.061417881763607e+53 and 3.061417881763607e+53

# Invertida
# att_estimation 0.00026502779560414884
# att_estimation_var 0.016544702072964695
# conf -2.8085130649762966e+77
# The estimated ATT is 0.00026502779560414884 IDR
# The 95% confidence interval is between -2.8085130649762966e+77 and 2.8085130649762966e+77


# Compute the estimated ATT
# est_att = np.mean(matched['spending'] - matched['spending_match'])

# Computing the variance, breaking it down to two terms
# first_term_var = np.mean((matched['spending'] - matched['spending_match'] - est_att)**2)
# second_term_var = sum(multiple_matches['size']*(multiple_matches['size'] - 1)*(multiple_matches['spending'] - multiple_matches['spending_match'])**2/2)/len(treated)
# est_var = first_term_var + second_term_var# Finally, compute the 95% confidence interval with n1 + n2 - 2 degrees of freedom
# from scipy.stats import t
# lb = est_att + t.ppf(0.025, 2 * len(treated) - 2) * np.sqrt(est_var)
# ub = est_att - t.ppf(0.025, 2 * len(treated) - 2) * np.sqrt(est_var)