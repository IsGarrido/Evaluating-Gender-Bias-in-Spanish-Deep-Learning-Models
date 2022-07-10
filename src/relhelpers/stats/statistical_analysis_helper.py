import datetime
from scipy.stats import wilcoxon, mannwhitneyu, shapiro, ttest_rel
import relhelpers.io.log_helper as _log

# https://pythonfordatascienceorg.wordpress.com/wilcoxon-sign-ranked-test-python/
# https://machinelearningmastery.com/nonparametric-statistical-significance-tests-in-python/
class StatisticalAnalysisHelper:


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
        stat, p = StatisticalAnalysisHelper.wilcoxon_paired(before, after)
        _log.log_print('[WCX   ] Statistics=' + str(stat) + ' p=' + str(p) )

        # interpret
        if p > alpha:
            _log.log_print('[WCX  ✔] Same distribution (fail to reject H0)')
        else:
            _log.log_print('[WCX   ] Different distribution (reject H0)')

    # Mann-Whitney U Test
    '''
        Fail to Reject H0: Sample distributions are equal.
        Reject H0: Sample distributions are not equal.
    '''

    def mann_whitney_u_test(before, after):
        stat, p = mannwhitneyu(before, after)
        return stat, p

    def mann_whitney_u_test_label(before, after, alpha = 0.05):

        stat, p = StatisticalAnalysisHelper.mann_whitney_u_test(before, after)

        _log.log_print('[MANN  ] Statistics=' + str(stat) + ' p=' + str(p) )

        if p > alpha:
            _log.log_print('[MANN ✔] Same distribution (fail to reject H0)')
        else:
            _log.log_print('[MANN  ] Different distribution (reject H0)')


    def t_test_normal(before, after, alpha = 0.05):

        difference = []
        zip_object = zip(before, after)

        for list1_i, list2_i in zip_object:
            difference.append(list1_i - list2_i)

        stat, p = shapiro(difference)

        _log.log_print('[SHAP  ] Statistics=' + str(stat) + ' p=' + str(p))

        if p >= alpha:
            _log.log_print('[SHAP ✔] p >= alpha, Is normal distribution')
            StatisticalAnalysisHelper.t_test_label(before, after, alpha)
        else:
            _log.log_print('[SHAP  ] p < alpha, Is NOT normal distribution')


    def t_test(before, after):
        stat, p = ttest_rel(before, after)
        return stat, p


    def t_test_label(before, after, alpha):
        statistic, p = ttest_rel(before, after)
        if p > alpha:
            _log.log_print('[TSTU ✔] Same distribution (fail to reject H0)')
        else:
            _log.log_print('[TSTU  ] Different distribution (reject H0)')


    def run_tests_labeled(before, after):

        _log.log_print("Test results for " + str(len(before)) + ", " + str(len(before)) + " elementos " )

        try:
            StatisticalAnalysisHelper.wilcoxon_paired_label(before, after)
        except:
            _log.log_print("No se ha podido ejecutar wilcoxon")

        try:
            StatisticalAnalysisHelper.mann_whitney_u_test_label(before, after)
        except:
            _log.log_print("No se ha podido ejecutar whitney")

        try:
            StatisticalAnalysisHelper.t_test_normal(before, after)
        except:
            _log.log_print("No se ha podido ejecutar ttest")

        _log.log_print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        _log.log_print("\n\n")

        return _log.get_log()