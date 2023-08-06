import pkgutil
import random
import pandas
import numpy as np
from numpy.matlib import randn, rand
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import io

def get_adult():
    return pandas.read_csv(data_path("adult.csv", elem="real"), encoding='utf8')


def get_name_proxy_data():
    return pandas.read_csv(data_path("prob_race_given_surname_2010.csv", elem='proxy'))


def get_name_of_race(race):
    """
    :param race: 'white', 'black', 'api', 'native', 'multiple', 'hispanic'
    :return: names of a certain race
    """
    data = get_name_proxy_data()
    race_list = {el: i for i, el in enumerate(list(data.drop(columns=['name']).columns.to_numpy()))}
    races = np.argmax(data.drop(columns=['name']).to_numpy(), axis=1)
    names_of_races = {}
    for r in race_list.values():
        names = data[['name']][races == r]
        names_of_races[r] = np.squeeze(names.to_numpy(), -1).tolist()

    res = []
    for rr in race:
        chosen_name = random.choice(names_of_races[race_list[rr]])
        res.append(chosen_name)
    return res


def one_hot_cat_vars(df, df_cols):
    """
    Adds new columns to hot encode every categorical values.
    :param df: dataframe to hot encode
    :param df_cols: cathegorical columns
    :return: new dataframe with hot encoded values
    """
    if len(df_cols) == 0:
        return df
    df_1 = df.drop(columns=df_cols, axis=1)
    df_2 = pd.get_dummies(df[df_cols])

    return (pd.concat([df_1, df_2], axis=1, join='inner'))


def predict_missing_values_for_column(dtf, unknown_val, column):
    test_data = dtf[(dtf[column].values == unknown_val)].copy()

    train_data = dtf[(dtf[column].values != unknown_val)].copy()
    train_label = train_data[column]

    test_data.drop(columns=[column], inplace=True)
    train_data.drop(columns=[column], inplace=True)

    train_data = one_hot_cat_vars(train_data, train_data.select_dtypes('category').columns)
    test_data = one_hot_cat_vars(test_data, test_data.select_dtypes('category').columns)

    log_reg = LogisticRegression()
    log_reg.fit(train_data, train_label)
    log_reg_pred = log_reg.predict(test_data)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train_data, train_label)
    clf_pred = clf.predict(test_data)

    r_forest = RandomForestClassifier(n_estimators=10)
    r_forest.fit(train_data, train_label)
    r_forest_pred = r_forest.predict(test_data)

    majority_class = dtf[column].value_counts().index[0]

    pred_df = pd.DataFrame({'RFor': r_forest_pred, 'DTree': clf_pred, 'LogReg': log_reg_pred})
    overall_pred = pred_df.apply(lambda x: x.value_counts().index[0] if x.value_counts()[0] > 1 else majority_class,
                                 axis=1)

    dtf.loc[(dtf[column].values == unknown_val), column] = overall_pred.values

    return dtf


def get_adult_with_name_and_income():
    adult_data = get_adult()

    adult_data.dropna(inplace=True)

    new_race_col = adult_data['race'].replace({
        "White": "white",
        "Black": "black",
        "Asian-Pac-Islander": "api",
        "Other": "multiple",
        "Amer-Indian-Eskimo": "native"
    }).tolist()

    for col in set(adult_data.columns) - set(adult_data.describe().columns):
        adult_data[col] = adult_data[col].astype('category')

    adult_data = predict_missing_values_for_column(adult_data, '?', 'workclass')
    adult_data = predict_missing_values_for_column(adult_data, '?', 'occupation')
    adult_data = predict_missing_values_for_column(adult_data, '?', 'native.country')

    # Resetting the categories
    adult_data['workclass'] = adult_data['workclass'].cat.remove_categories('?')
    adult_data['occupation'] = adult_data['occupation'].cat.remove_categories('?')
    adult_data['native.country'] = adult_data['native.country'].cat.remove_categories('?')

    edu_level = {}
    for x, y in adult_data[['education.num', 'education']].drop_duplicates().itertuples(index=False):
        edu_level[y] = x

    income_labl = adult_data['income']

    adult_data_noinc = adult_data.drop(columns=['income'])

    adult_cat_1hot = pd.get_dummies(adult_data_noinc.select_dtypes('category'))
    adult_non_cat = adult_data_noinc.select_dtypes(exclude='category')

    adult_data = pd.concat([adult_non_cat, adult_cat_1hot], axis=1, join='inner')

    scaler = StandardScaler()
    adult_data[adult_data.columns] = scaler.fit_transform(adult_data[adult_data.columns])

    w = rand(adult_data.shape[1], 1)
    i = np.array(np.power(np.squeeze(np.dot(adult_data, w), -1), 2)) * 100

    income_val = np.random.normal(25000, 10000, adult_data.shape[0])
    ll = income_labl == '>50K'
    income_val[ll] = np.random.normal(75000, 10000, adult_data.shape[0])[ll]
    income_val = np.squeeze(np.array(np.add(income_val, i)), 0)

    adult_data['name'] = get_name_of_race(new_race_col)
    adult_data['income'] = np.zeros_like(income_labl)
    adult_data['income'][income_labl == '>50K'] = 1
    adult_data['income_val'] = income_val

    return adult_data
#%%
# ddd = get_adult()
