# https://pythonfordatascienceorg.wordpress.com/wilcoxon-sign-ranked-test-python/
# https://machinelearningmastery.com/nonparametric-statistical-significance-tests-in-python/
from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu
from src.LogHelper import LogHelper
l = LogHelper()
# Si p > 0.05 -> Reject null hypothesis in support of the alternative

'''
The p-value can be interpreted in the context of a chosen significance level called alpha.
A common value for alpha is 5% or 0.05. If the p-value is below the significance level,
then the test says there is enough evidence to reject the null hypothesis and that the samples
were likely drawn from populations with differing distributions.


p <= alpha: reject H0, different distribution.
p > alpha: fail to reject H0, same distribution.

'''
def wilcoxon_paired(before, after):
    w, p = wilcoxon(before, after)
    return w, p

def wilcoxon_paired_label(before, after, alpha = 0.05):
    stat, p = wilcoxon_paired(before, after)
    l.log_print('[WCX] Statistics=%.3f, p=%.3f' % (stat, p))

    # interpret
    if p > alpha:
        l.log_print('[WCX ✔] Same distribution (fail to reject H0)')
    else:
        l.log_print('[WCX] Different distribution (reject H0)')










# Mann-Whitney U Test
'''
    Fail to Reject H0: Sample distributions are equal.
    Reject H0: Sample distributions are not equal.
'''

def mann_whitney_u_test(before, after):
    stat, p = mannwhitneyu(before, after)
    return stat, p

def mann_whitney_u_test_label(before, after, alpha = 0.05):

    stat, p = mann_whitney_u_test(before, after)

    l.log_print('[MANN] Statistics=%.3f, p=%.3f' % (stat, p))

    if p > alpha:
        l.log_print('[MANN ✔] Same distribution (fail to reject H0)')
    else:
        l.log_print('[MANN] Different distribution (reject H0)')


def run_tests_labeled(before, after):
    try:
        wilcoxon_paired_label(before, after)
    except:
        l.log_print("No se ha podido ejecutar wilcoxon")

    try:
        mann_whitney_u_test_label(before, after)
    except:
        l.log_print("No se ha podido ejecutar whitney")

    l.log_print("\n\n")
    return l.get_log()