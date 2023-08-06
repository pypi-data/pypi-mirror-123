import io
import random
import re

import numpy as np
import pandas as pd
import tensorflow as tf
import unidecode
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from transliterate import translit

from tuttusa_datasets.utils import data_path, load_synth, store_syth

gram_len = 2
maxlen = 7

ETHNICITIES = ["white", "black", "arab", "api", "hispanic", "native"]


def split_to_ngrams(name, gram_len):
    name_size = len(name) if isinstance(name, str) else tf.shape(name)
    return " ".join([name[i:i + gram_len] for i in range(0, name_size, gram_len)])


def preprocess_df_x(df, tokenizer, maxlen, gram_len):
    names = [e if isinstance(e, str) else "" for e in df['name'].values.tolist()]
    X = [split_to_ngrams(n, gram_len) for n in names]
    X = tokenizer.texts_to_sequences(X)
    X = pad_sequences(X, maxlen=maxlen)
    return X


def preprocess_x(names, gram_len=gram_len, maxlen=maxlen, char_level=False):
    tokenizer = tokenizer2(char_level=char_level)
    X = [split_to_ngrams(n, gram_len) for n in names]
    X = tokenizer.texts_to_sequences(X)
    X = pad_sequences(X, maxlen=maxlen)
    return X


def preprocess_y(df, num_classes):
    y = np.argmax(df.drop(columns=["name"]).values, axis=1)
    y = to_categorical(y, num_classes)
    return y


def clean_text(all_txt):
    repla = {'ʻ': '', 'ọ': 'o', 'ñ': 'n', 'ị': 'i', 'ǐ': 'i', 'ð': 'o', 'ş': 's', 'ữ': 'u', 'ế': 'e', 'ý': 'y',
             'ả': 'a', 'ǒ':'o',
             'ư': 'u', 'ǜ':'u', 'ǚ':'u', 'þ': 'b',
             'ő': 'o', 'å': 'a', 'ė': 'e', 'ă': 'a', 'ú': 'u', 'ồ': 'o', 'ằ': 'a', 'ž': 'z', 'ł': 'l', 'ũ': 'u',
             'ä': 'a', 'ǎ':'a', 'ğ': 'g',
             'ģ': 'g', 'ń': 'n', 'ö': 'o', 'ɗ': 'd', 'č': 'c', 'ʉ': 'u', 'ì': 'i', 'ề': 'e', 'ờ': 'o',
             'ż': 'z', 'ľ': 'l', 'ø': 'o', 'ứ': 'u', 'ǔ':'u', 'ķ': 'k', 'ơ': 'o', 'š': 's', 'ầ': 'a', 'ó': 'o', 'ƙ': 'k',
             'ợ': 'o', 'ę': 'e', 'ě':'e', 'ț': 't',
             'ș': 's', 'ē': 'e', 'ū': 'u', 'ạ': 'a', 'ś': 's', 'ī': 'i', 'ÿ':'y',
             'ỹ': 'y', 'ą': 'a', 'đ': 'd', 'õ': 'o', 'ņ': 'n', 'ỳ': 'y', 'ā': 'a', 'ļ': 'l', 'ệ': 'e', 'ň': 'n',
             'ō': 'o'}
    n_all_txt = []
    for txt in all_txt:
        if isinstance(txt, str):
            txt = re.sub(r"^[-+]?[0-9]+$", '', txt)
            txt = txt.lower()
            txt = re.sub(r"[$&+,:;=?@#|'<>.-^*()%!]", '', txt)
            txt = txt.replace('(', '')
            txt = txt.replace(')', '')
            txt = txt.replace('[', '')
            txt = txt.replace(']', '')
            txt = txt.replace('\'', '')
            txt = txt.replace('.', '')
            txt = txt.replace(',', '')
            txt = txt.replace(';', '')
            txt = txt.replace('`', '')
            txt = txt.replace('é', 'e')
            txt = txt.replace('è', 'e')
            txt = txt.replace('ë', 'e')
            txt = txt.replace('ê', 'e')
            txt = txt.replace('â', 'a')
            txt = txt.replace('ã', 'a')
            txt = txt.replace('á', 'a')
            txt = txt.replace('ô', 'o')
            txt = txt.replace('ò', 'o')
            txt = txt.replace('ç', 'c')
            txt = txt.replace('î', 'i')
            txt = txt.replace('í', 'i')
            txt = txt.replace('æ', 'ae')
            txt = txt.replace('œ', 'oe')
            txt = txt.replace('û', 'u')
            txt = txt.replace('à', 'a')
            txt = txt.replace('ù', 'u')
            txt = txt.replace('ë', 'e')
            txt = txt.replace('ï', 'i')
            txt = txt.replace('ü', 'u')
            txt = txt.replace('©', '')
            txt = txt.replace('rã', '')
            txt = txt.replace('™', '')
            txt = txt.replace('d\'', '')
            txt = txt.replace('-', '')
            txt = txt.replace('_', '')
            txt = txt.replace('’', '')
            txt = txt.replace('"', '')
            txt = txt.replace('\n', '')
            txt = txt.replace('\u3000', '')
            txt = txt.replace('ち', '')
            txt = txt.replace('み', '')
            txt = txt.replace('き', '')
            txt = txt.replace('り', '')
            txt = txt.replace('便', '')
            txt = txt.replace('い', '')
            txt = txt.replace('片', '')
            txt = txt.replace('し', '')
            txt = txt.replace('に', '')
            txt = txt.replace('ひ', '')
            txt = txt.replace('，', '')
            txt = txt.replace(' ', '')

            for e in repla:
                txt = txt.replace(e, repla[e])

            n_all_txt.append(txt)

    return n_all_txt


def get_tokenizer(columns=['white', 'black', 'api', 'hispanic', 'native', 'multiple']):
    tokenizer = Tokenizer(
        num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True,
        split=' ', char_level=False, oov_token=None, document_count=0)

    df = pd.read_csv(data_path("prob_race_given_surname_2010.csv", elem="proxy"))

    df = df.dropna()

    # data reiweghing for classes which are very unbalanced

    columns_to_drop = list(set(list(df.columns)).difference(set(columns + ["name"])))

    df.drop(columns=columns_to_drop, inplace=True)

    means = {"white": 0.05, "black": 0.6, "api": 0.6, "native": 0.9,
             "multiple": 0.9, "hispanic": 0.6}

    means = [means[el] for el in columns]
    args_kk = np.array([means[i] for i in np.argmax(df.drop(columns=["name"]).values, axis=1)])

    msk = np.random.rand(len(df)) < 0.8
    train_df = df[msk]
    test_df = df[~msk]
    train_df = train_df.sample(1000000, weights=args_kk[msk], replace=True)

    names = [e if isinstance(e, str) else "" for e in df['name'].values.tolist()]
    split_names = [split_to_ngrams(n, gram_len) for n in names]

    tokenizer.fit_on_texts(split_names)

    return tokenizer, df, train_df, test_df


def process_census_data(columns=['white', 'black', 'api', 'hispanic', 'native', 'multiple']):
    tokenizer, df, train_df, test_df = get_tokenizer(columns)

    vocab_len = len(tokenizer.word_index) + 1
    num_classes = np.unique(np.argmax(df.drop(columns=["name"]).values, axis=1)).shape[0]

    X_train = preprocess_df_x(train_df, tokenizer, maxlen, gram_len)
    X_test = preprocess_df_x(test_df, tokenizer, maxlen, gram_len)

    y_train = preprocess_y(train_df, num_classes)
    y_test = preprocess_y(test_df, num_classes)

    def process_model_out(out):
        return np.take(train_df.drop(columns=['name']).columns, out)

    races = {el: i for i, el in enumerate(df.drop(columns='name').columns.tolist())}

    return X_train, X_test, y_train, y_test, vocab_len, num_classes, process_model_out, races


def tokenizer2(char_level=False):
    data = get_names_data()

    tokenizer = Tokenizer(
        num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True,
        split=' ', char_level=char_level, oov_token=None, document_count=0)

    data = [split_to_ngrams(n, gram_len) for n in data[0]]

    tokenizer.fit_on_texts(data)

    return tokenizer


def get_black_names():
    data = pd.read_csv(data_path("black/african_lastname.csv", elem="proxy")).dropna()['name'].tolist()
    data = [el.split(" ")[1].replace(":", "") for el in data]
    data1 = pd.read_csv(data_path("black/data.csv", elem="proxy")).dropna()["name"].tolist()
    data2 = pd.read_csv(data_path("black/data1.csv", elem="proxy")).dropna()["slave_name"].tolist()
    data3 = pd.read_csv(data_path("black/data2.csv", elem="proxy"), names=["name"]).dropna()["name"].tolist()

    all_data = data + data1 + data2 + data3

    res = list(set(clean_text(all_data)))
    return res


def get_native_names():
    data = pd.read_csv(data_path("native/data.csv", elem="proxy"))
    res = clean_text(data['name'].tolist())
    return res


def get_arab_names():
    data = pd.read_csv(data_path("arab/arab_names.csv", elem="proxy")).dropna()['name'].tolist()
    data1 = pd.read_csv(data_path("arab/data.csv", elem="proxy")).dropna()['name'].tolist()
    data2 = pd.read_csv(data_path("arab/females_en.csv", elem="proxy")).dropna()['Name'].tolist()
    data3 = pd.read_csv(data_path("arab/males_en.csv", elem="proxy")).dropna()['Name'].tolist()
    all_data = data + data1 + data2 + data3
    res = list(set(clean_text(all_data+all_data)))
    return res


def get_api_names():
    chinesedata = pd.read_csv(data_path("api/chinese/chinese.csv", elem="proxy"))
    chinesedata.dropna()
    chinesedata_res = [unidecode.unidecode(re.search("(?<=\()(.*)(?=\))", el).group()) for el in
                       chinesedata['name'].tolist()]
    chinese_vocab = []
    with io.TextIOWrapper(data_path("api/chinese/vocabulary.txt", elem="proxy"), encoding="utf-8") as f:
        for line in list(f):
            chinese_vocab.append(line.split("\'")[1])

    japanesedata = pd.read_csv(data_path("api/japanese/japanese.csv", elem="proxy"))
    japanesedata.dropna()
    japanesedata_res = [re.search("(?<=\.)(.*)(?=:)", el).group().replace(" ", "").lower() for el in
                        japanesedata['name'].tolist()]

    japanesenames = []
    with io.TextIOWrapper(data_path("api/japanese/japanesenames.txt", elem="proxy"), encoding="utf-8") as f:
        for line in list(f):
            try:
                japanesenames.append(line.split("\t")[1].replace('\n', ''))
            except:
                pass

    koreannames = []
    with io.TextIOWrapper(data_path("api/korean/names.txt", elem="proxy"), encoding="utf-8") as f:
        for line in list(f):
            koreannames.append(line.replace('\n', ''))

    data1 = pd.read_csv(data_path("api/data.csv", elem="proxy")).dropna()['name'].tolist()

    all_data = chinesedata_res + japanesedata_res + data1 + chinese_vocab + japanesenames + koreannames

    res = list(set(clean_text(all_data)))

    return res


def get_hispanic_names():
    def split_names(names_list):
        n_data = []
        for el in names_list:
            n_data.extend(el.split(" "))

        return n_data

    spanish_names = pd.read_csv(data_path("hispanic/spanish_names.csv", elem="proxy")).dropna()["names"].tolist()
    spanish_names = [el.split(" ")[1].replace(":", '') for el in spanish_names]
    data0 = pd.read_csv(data_path("hispanic/brazilian-names-and-gender.csv", elem="proxy")).dropna()["Name"].tolist()
    data1 = pd.read_csv(data_path("hispanic/data.csv", elem="proxy")).dropna()["name"].tolist()
    data2 = pd.read_csv(data_path("hispanic/female_names.csv", elem="proxy")).dropna()["name"].tolist()
    data2 = split_names(data2)
    data3 = pd.read_csv(data_path("hispanic/male_names.csv", elem="proxy")).dropna()["name"].tolist()
    data3 = split_names(data3)

    all_data = spanish_names + data0 + data1 + data2 + data3

    res = list(set(clean_text(all_data)))

    return res


def get_white_names():
    def exract_english_names():
        import pathlib
        ooo = []
        lll = pathlib.Path.cwd().joinpath("bayesiantarnet/research/data/datasets/proxy/white/english/names").iterdir()
        for ll in lll:
            ooo.extend(pd.read_csv(ll.as_posix(), sep=",", names=["names", "de", "ty"])['names'].tolist())

        ooo = set(ooo)

        ooo = pd.DataFrame(data={"name": ooo})

        ooo.to_csv("english_names.csv")

    quebec_names1 = pd.read_csv(data_path("white/frenchcanadian/1000_noms_quebec.csv", elem="proxy"))
    quebec_names1 = quebec_names1[quebec_names1.columns[2:]].apply(
        lambda x: ','.join(x.dropna().astype(str)),
        axis=1
    ).tolist()

    quebec_names2 = pd.read_csv(data_path("white/frenchcanadian/frenchcanada2.csv", elem="proxy")).dropna()
    quebec_names2_list = []
    for el in quebec_names2['name'].tolist():
        try:
            quebec_names2_list.append(el.split(" ")[0])
        except:
            pass

    quebec_names3 = pd.read_csv(data_path("white/frenchcanadian/frenchcanadanames.csv", elem="proxy")).dropna()[
        "names"].tolist()

    quebec_names = quebec_names1 + quebec_names2_list + quebec_names3

    german_names = []
    with io.TextIOWrapper(data_path("white/german/german_names.txt", elem="proxy"), encoding="utf-8") as f:
        for line in list(f):
            try:
                german_names.append(line.split(" ")[0])
            except:
                pass

    italian_names1 = pd.read_csv(data_path("white/italian/italian-first-names1.csv", elem="proxy")).dropna()
    italian_names2 = pd.read_csv(data_path("white/italian/italian-first-names2.csv", elem="proxy")).dropna()
    italian_names = italian_names1['name'].tolist() + italian_names2['name'].tolist()

    english_names = pd.read_csv(data_path("white/english/english_names.csv", elem="proxy")).dropna()['name'].tolist()

    french_names = pd.read_csv(data_path("white/french/french_names.csv", elem="proxy"), encoding='latin1').dropna()[
        "name"].tolist()

    russian_names = pd.read_csv(data_path("white/russian/names.csv", elem="proxy")).dropna()
    russian_names = [translit(el, "ru", reversed=True) for el in russian_names['name'].tolist()]

    data1 = pd.read_csv(data_path("white/data.csv", elem="proxy"))['name'].tolist()

    all_data = [data1, french_names, quebec_names, english_names, russian_names]
    res = make_minimal_res(all_data)

    return res


def make_minimal_res(data_list):
    all_data = [list(set(clean_text(el))) for el in data_list]

    min_val = min([len(el) for el in all_data])
    all_data = [el[:min_val] for el in all_data]
    all_data = sum(all_data, [])

    res = list(set(all_data))

    return res


def names_data(remake):
    data_name = "names_data.pk"

    if remake:
        names = {
            "black": get_black_names()[:17000],
            "arab": get_arab_names(),
            "api": get_api_names(),
            "white": get_white_names(),
            "hispanic": get_hispanic_names(),
            "native": get_native_names()
        }

        store_syth(names, data_name)
    else:
        names = load_synth(data_name)

    return names


def replace_race_with_name(races_list):
    names = names_data(False)
    return [random.choice(names[el]) for el in races_list]


def get_names_data(columns=ETHNICITIES, remake=False):
    names = names_data(remake)
    x_cols = []
    y_cols = []
    for el in columns:
        if el in list(names):
            x_cols.append(names[el])
            y_cols.append(np.full_like(names[el], int(columns.index(el))))
        else:
            y_cols.append(np.full_like(list(names.values())[0], int(columns.index(el))))

    X = np.concatenate(x_cols)
    y = tf.one_hot(np.concatenate(y_cols), len(columns)).numpy()

    indexes = np.arange(0, X.shape[0])

    np.random.shuffle(indexes)

    X = np.take(X, indexes)
    y = np.take(y, indexes, axis=0)

    return X, y


def get_training_names_data_lstm(columns=ETHNICITIES, process_name=True, remake=False):
    X, y = get_names_data(columns, remake)

    if process_name:
        X = preprocess_x(X)

    random_suffle = np.arange(X.shape[0])
    np.random.shuffle(random_suffle)

    X = np.take(X, random_suffle, axis=0)
    y = np.take(y, random_suffle, axis=0)

    X_test, X_train = X[:int(X.shape[0] * 0.2)], X[int(X.shape[0] * 0.2):]
    y_test, y_train = y[:int(X.shape[0] * 0.2)], y[int(X.shape[0] * 0.2):]

    def process_model_out(out):
        return np.take(columns, out)

    races = {el: i for i, el in enumerate(columns)}

    return X_train, X_test, y_train, y_test, len(columns), process_model_out, races


def get_training_names_data_cnn(columns=ETHNICITIES):
    X, y = get_names_data(columns)

    X = preprocess_x(X, gram_len=1, maxlen=15, char_level=True)

    random_suffle = np.arange(X.shape[0])
    np.random.shuffle(random_suffle)

    X = np.take(X, random_suffle, axis=0)
    y = np.take(y, random_suffle, axis=0)

    X_test, X_train = X[:int(X.shape[0] * 0.2)], X[int(X.shape[0] * 0.2):]
    y_test, y_train = y[:int(X.shape[0] * 0.2)], y[int(X.shape[0] * 0.2):]

    def process_model_out(out):
        return np.take(columns, out)

    races = {el: i for i, el in enumerate(columns)}

    return X_train, X_test, y_train, y_test, len(columns), process_model_out, races


def get_training_names_data_xgboost(columns=ETHNICITIES):
    tokenizer = tokenizer2()

    def make_x_boost_data(x_train):
        x_data = []
        for el in x_train:
            x_row = list(np.zeros(len(tokenizer.index_word) + 1))
            for e in el:
                x_row[e] += 1
            x_data.append(x_row)

        x_data = np.array(x_data).T

        x_data = {el: x_data[i] for el, i in tokenizer.word_index.items()}

        x_data = pd.DataFrame(data=x_data)

        return x_data

    X, y = get_names_data(columns)

    X = preprocess_x(X)

    random_suffle = np.arange(X.shape[0])
    np.random.shuffle(random_suffle)

    X = np.take(X, random_suffle, axis=0)
    y = np.take(y, random_suffle, axis=0)

    X_test, X_train = X[:int(X.shape[0] * 0.2)], X[int(X.shape[0] * 0.2):]
    y_test, y_train = y[:int(X.shape[0] * 0.2)], y[int(X.shape[0] * 0.2):]

    X_train = make_x_boost_data(X_train)
    X_test = make_x_boost_data(X_test)

    y_train = np.argmax(y_train, axis=1)
    y_test = np.argmax(y_test, axis=1)

    def process_model_out(out):
        return np.take(columns, out)

    races = {el: i for i, el in enumerate(columns)}

    return X_train, X_test, y_train, y_test, len(columns), process_model_out, races

# def get_spanish():
# data1 = pd.read_csv(data_path("hispanic/female_names.csv", elem="proxy"))
# data2 = pd.read_csv(data_path("hispanic/male_names.csv", elem="proxy"))
#
# data1['percent'] = np.array(data1['frequency'].tolist()) / np.sum(data1['frequency'].tolist()) * 100
# data2['percent'] = np.array(data2['frequency'].tolist()) / np.sum(data2['frequency'].tolist()) * 100
#
# name1 = data1['name'][data1['percent'] >= 0.003].tolist()
# name2 = data2['name'][data2['percent'] >= 0.003].tolist()
#
# all_data = name1 + name2
#
# ll = []
# for el in all_data:
#     try:
#         ll.extend(el.split(" "))
#     except:
#         pass
# all_data = set(ll)
#
# res = clean_text(all_data)

# return res
# get_names_data()
