from scipy.stats import pearsonr, pointbiserialr, chi2_contingency
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from statistics import mean
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import MinMaxScaler, StandardScaler
# from sklearn.decomposition import PCA
# from lightgbm import LGBMClassifier
# from catboost import CatBoostClassifier
# from xgboost import XGBClassifier
# from sklearn.ensemble import VotingClassifier
# from sklearn.model_selection import GridSearchCV
# from sklearn.preprocessing import LabelEncoder, OrdinalEncoder


def univar_analysis(df):
    for i in df:
        if df[i].dtype == 'object':
            sns.barplot(df[i].value_counts().index, df[i].value_counts())
            plt.title(i)
            plt.show()
        else:
            fig, ax = plt.subplots(1, 2, figsize=(10, 4))
            fig.tight_layout()
            ax[0].hist(df[i])
            ax[0].set_title(i)
            ax[1].boxplot(df[i])
            ax[1].set_title(i)
            plt.show()


def dichotomous_categorical_visual(df, target):
    if len(df[target].unique()) == 2:
        df_0 = df[df[target] == 0]
        df_1 = df[df[target] == 1]
        for i in df:
            if df[i].dtype == 'object':
                fig, axes = plt.subplots(1, 2, figsize=(16, 6))
                pd.crosstab(df_0[target], df_0[i]).plot(kind='bar', ax=axes[0])
                pd.crosstab(df_1[target], df_1[i]).plot(kind='bar', ax=axes[1])
    else:
        print("Your target variable is not dichotomous!")


def categorical_visual(x, y, data, kind, hue=None):
    sns.catplot(x, y, hue, data, kind=kind)


def categorical_multivariate_visual(x, y, hue, data, kind):
    sns.catplot(x, y, hue, data, kind=kind)


def continuous_visual(df, target):
    sns.set(rc={'figure.figsize': (16, 10)})
    df_float = df.select_dtypes(['float', 'int'])
    for i, n in enumerate(df_float):
        sns.boxplot(y=target, x=df[n], data=df)
        plt.show()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def chi2_test(df_cat, target_name):
    chi2_summary = []
    for i in df_cat:
        (chi2, p, dof, _) = chi2_contingency(
            pd.crosstab(df_cat[target_name], df_cat[i]))
        score_to_add = {}
        score_to_add['var'] = i
        score_to_add['chi_square_stat'] = chi2
        score_to_add['p-value'] = p
        score_to_add['dof'] = dof
        chi2_summary.append(score_to_add)
    df_chi2 = pd.DataFrame(chi2_summary)

    return df_chi2


def pbs_test(df_num, target_name):
    num_summary = []
    for i in df_num:
        pbs = pointbiserialr(df_num[i], df_num[target_name])
        score_to_add = {}
        score_to_add['var'] = i
        score_to_add['pbs corr'] = pbs[0]
        score_to_add['pbs p-value'] = pbs[1]
        num_summary.append(score_to_add)
    df_num = pd.DataFrame(num_summary)

    return df_num


def pearson_test(df_num, target_name):
    num_summary = []
    for i in df_num:
        pbs = pearsonr(df_num[i], df_num[target_name])
        score_to_add = {}
        score_to_add['var'] = i
        score_to_add['pearson corr'] = pbs[0]
        score_to_add['pearson p-value'] = pbs[1]
        num_summary.append(score_to_add)
    df_num = pd.DataFrame(num_summary)

    return df_num


def outlier_treatment():  # maybe don't need this
    pass


def fill_null():
    pass


def normalisation():
    pass


def standardisation():
    pass


def one_hot_encoding():
    pass


def label_encoding():
    pass


def ordinal_encoding():
    pass


def pca():
    pass

# addigional boosted trees models and classifiers?
# gridsearch?
