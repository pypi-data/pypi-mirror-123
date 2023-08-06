# %%
import copy
import hashlib
import inspect
import math
import random
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.stats import gaussian_kde
from sklearn.datasets import make_regression
from sklearn.datasets import make_blobs

from tuttusa_datasets.models import Dataset
from tuttusa_datasets.utils import load_synth, data_path, store_syth
from tuttusa_datasets.proxy_data import preprocess_x


def get_test_data(t_labels=["w", "b", "c", "d"], n_sample=10000):
    x, y = make_regression(random_state=10, n_targets=len(t_labels), n_features=6, n_samples=n_sample)
    t = np.array([random.choice(list(range(len(t_labels)))) for _ in range(n_sample)])
    if len(t_labels) != 1:
        y_t = np.array([y[i, int(el)] for i, el in enumerate(np.squeeze(t))])
    else:
        y_t = copy.deepcopy(y)
    x_train, x_test = x[1000:], x[:1000]
    y_train, y_test = y_t[1000:], y_t[:1000]
    t_train, t_test = t[1000:], t[:1000]

    proxy = lambda x: x

    return x_train, y_train, x_test, y_test, t_train, t_test, t_labels, proxy, x, y, t, y_t


class GenerateData:

    @classmethod
    def make_protected_attribute(self, config, train_len, test_len):
        """
        makes the protected attribute along with the proxy
        :param config:
        :param train_len:
        :param test_len:
        :return:
        """

        def make_t(length):

            t_s = []
            for i, mino in enumerate(config.proportion.keys()):
                t_ = np.full((int(length * list(config.proportion.values())[i])), i)

                t_s = np.append(t_s, t_)

            np.random.shuffle(t_s)

            return t_s

        t_train = make_t(train_len)
        t_test = make_t(test_len)

        t = np.append(t_train, t_test)
        if len(t) < (train_len + test_len):
            t = np.append(t, t[:(train_len + test_len) - len(t)])
        t = np.expand_dims(t, -1)

        # to_chng_index = random.choices(list(range(t.shape[0])), k=int(t.shape[0] * config["corr"]))
        # for el in to_chng_index:
        #     t[el] = random.choice(list(set(range(len(config["percent"].keys()))).difference(t[el])))

        return t

    @classmethod
    def equalize_to_x_shape(self, x, t, y, labels):
        y_vals = OrderedDict({})
        for el, i in labels.items():
            vals = np.zeros(x.shape[0])
            vals[np.squeeze(t, -1) == i] = y[np.squeeze(t, -1) == i]
            y_vals[el] = np.expand_dims(vals, -1)

        return y_vals

    @classmethod
    def get_file_from_hash_params(self, params):
        file_name = "{}.pk".format(
            hashlib.md5(str((str(params.get('config')), params.get('percent_test'), params.get('n_samples'),
                             params.get('noise'), params.get('factor'), params.get('nb_clusters'))).encode(
                'utf-8')).hexdigest())

        file = load_synth(file_name) if not params["remake"] else None

        return file, file_name

    @classmethod
    def synth_proxy(self, labels, corr):
        def proxy(t):
            rand_nb = tf.random.uniform(tf.shape(t), minval=0, maxval=1)
            to_chang = tf.less_equal(rand_nb, 1 - corr)
            t = tf.where(to_chang, tf.cast(random.choices(labels, k=to_chang.shape[-1]), dtype=t.dtype), t)
            return t

        return proxy

    @classmethod
    def name_proxy(self, model_name, labels):
        labels = copy.deepcopy(labels)
        name_proxy_model = LSTMProxyModel()

        def proxy(t):
            t_vals = name_proxy_model(t)
            t_vals = name_proxy_model.filter_for_ethnicities(labels, t_vals)
            return tf.cast(tf.argmax(t_vals, axis=-1), dtype=tf.float32)

        return proxy

    @classmethod
    def replace_with_race_name(self, t, labels):
        name_t = [labels[int(el)] for el in t]
        name_t = replace_race_with_name(name_t)

        return name_t

    @classmethod
    def regression_data(self, config, percent_test=0.3, n_samples=1000, plot=True, remake=True):
        data, file_name = self.get_file_from_hash_params(inspect.getargvalues(inspect.currentframe())[3])

        if config.use_name_proxy:
            p = self.name_proxy(config.model_name, config.t_labels)
        else:
            p = self.synth_proxy(list(range(len(config.t_labels))), config.correlation)

        if data is None or remake:

            x, y = make_regression(random_state=10, n_targets=len(config.proportion), n_features=6,
                                   noise=config.noise_rate, n_samples=n_samples)

            y += config.base_y_val

            if config.noise_rate != 0:
                noise_args = np.random.choice(np.arange(x.shape[0]), int(x.shape[0] * config.shuffle_noise))

                new_noise_args = copy.deepcopy(noise_args)
                np.random.shuffle(new_noise_args)

                x[noise_args] = np.take(x, new_noise_args, axis=0)

            cut = int(n_samples * percent_test)

            # split dataset into train and test
            x_test, x_train = x[:cut], x[cut:]
            y_test, y_train = y[:cut], y[cut:]

            # recalibrate according to clusters

            t = self.make_protected_attribute(config, x_train.shape[0], x_test.shape[0])

            t_test, t_train = t[:cut], t[cut:]

            # add a number of changes to the dataset to exasperate disparity between the two groups

            if config.add_disparity is not None:
                y_train = y_train * config.add_disparity
                y_test = y_test * config.add_disparity
            if config.add_disparity is not None:
                y_train = y_train + config.add_disparity
                y_test = y_test + config.add_disparity

            if plot:
                plt.clf()
                df = pd.Series(np.random.randint(10, 50, len(config.proportion.keys())),
                               index=np.arange(1, len(config.proportion.keys()) + 1))
                cmap = plt.cm.tab10
                colors = cmap(np.arange(len(df)) % cmap.N)
                for el in range(len(config.proportion.keys())):
                    n, bins = np.histogram(y_test[:, el], 30)
                    density = gaussian_kde(y_test[:, el])
                    plt.plot(bins, density(bins), color=colors[el], label=str(el))
                plt.legend()
                plt.title("Real regression distribution")
                plt.savefig(data_path("regression_real_distr.jpg", "figure", action='save'))
                plt.show()

            # y_test = {el: np.expand_dims(y_test[:, i], -1) for i, el in enumerate(config["percent"].keys())}
            # y_train = {el: np.expand_dims(y_train[:, i], -1) for i, el in enumerate(config["percent"].keys())}

            y_test = [y_test[i, int(el)] for i, el in enumerate(np.squeeze(t_test, -1))]
            y_train = [y_train[i, int(el)] for i, el in enumerate(np.squeeze(t_train, -1))]

            # y_test = {el: np.expand_dims(y_test, -1) for i, el in enumerate(config["percent"].keys())}
            # y_train = {el: np.expand_dims(y_train, -1) for i, el in enumerate(config["percent"].keys())}

            y_test = np.array(y_test)
            y_train = np.array(y_train)

            if config.use_name_proxy:
                if config.process_proxy:
                    t_proxy_test = preprocess_x(self.replace_with_race_name(t_test, list(config.proportion)))
                    t_proxy_train = preprocess_x(self.replace_with_race_name(t_train, list(config.proportion)))
                else:
                    t_proxy_test = self.replace_with_race_name(t_test, list(config.proportion))
                    t_proxy_train = self.replace_with_race_name(t_train, list(config.proportion))
            else:
                t_proxy_test = copy.deepcopy(t_test)
                t_proxy_train = copy.deepcopy(t_train)

            labels = config.t_labels

            # res_data = [t_test, t_proxy_test, x_test, y_test, t_train, t_proxy_train, x_train, y_train, labels]

            res_dataset = Dataset(t_test=t_test, t_proxy_test=t_proxy_test, x_test=x_test, y_test=y_test, t_train=t_train,
                              t_proxy_train=t_proxy_train, x_train=x_train, y_train=y_train, labels=labels, proxy=p)

            # store_syth(res_data, file_name)

            # res_data.append(p)

            return res_dataset

        else:
            data = list(data)
            data.append(p)
            return data

    @classmethod
    def make_classification_data(self, config, plot=True, n_samples=1000, n_features=10, percent_test=0.3,
                                 remake=False):

        """
        generate one W for each class label and assign different proportions of this label to each protected attribute
        :param config:
        :param nb_clusters:
        :param cluster_prop:
        :param plot:
        :param n_samples:
        :param n_features:
        :param percent_test:
        :param remake:
        :return:
        """

        data, file_name = self.get_file_from_hash_params(inspect.getargvalues(inspect.currentframe())[3])

        p = self.synth_proxy(list(range(len(config["disp"]))), config['corr'])

        if data is None or remake:

            test_len = int(n_samples * percent_test)
            train_len = n_samples - test_len

            n_classes = len(config["disp"])

            x, cla = make_blobs(len(config["percent"]) * n_samples, n_features, len(config["disp"]),
                                cluster_std=1.5)

            t = self.make_protected_attribute(config, train_len, test_len)
            x_race = np.zeros((t.shape[0], x.shape[1]))
            y_race = np.zeros((t.shape[0]))

            for i, disp in enumerate(config["disp"].values()):
                race_pos = np.argwhere(t == i)[:, 0]
                race_sta_fin = [0]
                for dis_i, el in enumerate(disp):
                    start = race_sta_fin[dis_i]
                    end = math.floor((len(race_pos) * el) + race_sta_fin[dis_i])
                    cla_pos = np.random.choice(np.argwhere(cla == dis_i)[:, 0], end - start)
                    x_race[race_pos[start:end]] = x[cla_pos]
                    y_race[race_pos[start:end]] = cla[cla_pos]
                    race_sta_fin.append(end)

            random_suffle = np.arange(x_race.shape[0])
            np.random.shuffle(random_suffle)

            y_race = np.take(y_race, random_suffle)
            x_race = np.take(x_race, random_suffle, axis=0)
            t = np.take(t, random_suffle, axis=0)

            y_race = self.equalize_to_x_shape(x_race, t, y_race, {e: e_i for e_i, e in enumerate(list(config["disp"]))})

            cut = int(n_samples * percent_test)

            y_race = np.stack(y_race.values(), axis=1)
            if config['noise_rate'] != 0:
                noise_args = np.random.choice(np.arange(x_race.shape[0]), int(x_race.shape[0] * config['noise_rate']))

                new_noise_args = copy.deepcopy(noise_args)
                np.random.shuffle(new_noise_args)

                x_race[noise_args] = np.take(x_race, new_noise_args, axis=0)

            x_test, x_train = x_race[:cut], x_race[cut:]
            y_test, y_train = y_race[:cut], y_race[cut:]

            # np.unique(y_race[cut:][:, 0, :][np.squeeze(t, -1)[cut:] == 0], return_counts=True)

            if plot:
                plt.clf()
                df = pd.Series(np.random.randint(10, 50, len(config["percent"].keys())),
                               index=np.arange(1, len(config["percent"].keys()) + 1))
                cmap = plt.cm.tab10
                colors = cmap(np.arange(len(df)) % cmap.N)
                for el in range(len(config["percent"].keys())):
                    vals = np.unique(y_test[:, el, :][np.squeeze(t, -1)[:cut] == el], return_counts=True)
                    plt.scatter(vals[0], vals[1] / y_test[np.squeeze(t, -1)[:cut] == el].shape[0], color=colors[el],
                                label=str(el))
                plt.legend()
                plt.title("Real classification distribution")
                plt.ylim(top=1.2)
                plt.savefig(data_path("classification_real_distr.jpg", "figure"))
                plt.show()

            y_test = {el: np.expand_dims(y_test[:, i], -1) for i, el in enumerate(config["percent"].keys())}
            y_train = {el: np.expand_dims(y_train[:, i], -1) for i, el in enumerate(config["percent"].keys())}

            labels = list(config["percent"].keys())

            res_data = [t[:cut], x_test, y_test, t[cut:], x_train, y_train, n_classes, labels]

            store_syth(res_data, file_name)

            res_data.append(p)

            return res_data

        else:
            data = list(data)
            data.append(p)
            return data
