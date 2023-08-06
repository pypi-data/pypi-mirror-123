import io
import os
import pathlib
import pickle
import pkgutil
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from pydantic import BaseModel
import dload
import requests
from google.cloud import storage
from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.typing import List, Dict
from pydantic.utils import OrderedDict
from tqdm import tqdm

storage_crentials_path = "C:/Users/gen06917/OneDrive - ASFLC/Documents/maitrise-e53a8fa8a1ee.json"
main_bucket = "baysiantarnet"

main_data_path = pathlib.Path(__file__).absolute().parent.joinpath("datasets")

synth_data_path = main_data_path.joinpath("synthetic")
figure_path = main_data_path.joinpath("figures")
proxy_data_path = main_data_path.joinpath("proxy")
real_data_path = main_data_path.joinpath("real")
checkpoint_path = main_data_path.joinpath("saved_model")
analysis_saving_path = main_data_path.joinpath("previous_analysis")


def data_path(name, elem, action='load'):
    data_path = {
        "package": {
            "synth": "datasets/synthetic/{}".format(name),
            "figure": "datasets/figures/{}".format(name),
            "real": "datasets/real/{}".format(name),
            "proxy": "datasets/proxy/{}".format(name),
            "model": "datasets/saved_model/{}".format(name),
            "analysis": "datasets/previous_analysis/{}".format(name)
        },
        "research": {
            "synth": synth_data_path,
            "figure": figure_path,
            "real": real_data_path,
            "proxy": proxy_data_path,
            "model": checkpoint_path,
            "analysis": analysis_saving_path
        }
    }

    if action == 'load':
        if elem in ['model', 'analysis']:
            return data_path["research"][elem].joinpath(name).as_posix()
        try:
            return io.BytesIO(pkgutil.get_data(__name__, data_path["package"][elem]))
        except:
            return data_path["research"][elem].joinpath(name).as_posix()
    elif action == 'save':
        return data_path["research"][elem].joinpath(name).as_posix()


def store_syth(data, name, elem='synth'):
    path = data_path(name, elem=elem, action='save')
    with open(path, 'wb') as file:
        pickle.dump(data, file)
        file.close()


def load_synth(name, elem='synth'):
    path = data_path(name, elem=elem)
    if isinstance(path, str):
        with open(path, 'rb') as file:
            return pickle.load(file)
    else:
        return pickle.load(path)


def make_zip(tree_path, zip_path, mode='w', skip_empty_dir=False):
    with ZipFile(zip_path, mode=mode, compression=ZIP_DEFLATED) as zf:
        paths = [Path(tree_path)]
        while paths:
            p = paths.pop()
            if p.is_dir():
                paths.extend(p.iterdir())
                if skip_empty_dir:
                    continue
            zf.write(p, p.relative_to(tree_path))


def download_file(url, file):
    chunk_size = 1024
    r = requests.get(url, stream=True)
    pbar = tqdm(unit="B", total=int(r.headers['Content-Length']))
    for chunk in r.iter_content(chunk_size=chunk_size):
        if chunk:  # filter out keep-alive new chunks
            pbar.update(len(chunk))
            file.write(chunk)


def upload_data_to_cloud(blob_name):
    client = storage.Client.from_service_account_json(os.environ['storage_crentials_path'])
    bucket = client.get_bucket(main_bucket)
    blob = bucket.blob("data{}.zip".format(blob_name))

    new_file, filename = tempfile.mkstemp()
    make_zip(main_data_path, filename)
    blob.upload_from_filename(filename)

    os.close(new_file)


def download_data_from_cloud(blob_name):
    u = "https://storage.googleapis.com/{}/{}".format(main_bucket, "data{}.zip".format(blob_name))
    if main_data_path.exists():
        shutil.rmtree(main_data_path)
    main_data_path.mkdir()
    dload.save_unzip(u, main_data_path.as_posix(), delete_after=True)



