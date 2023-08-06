import pathlib
import pickle
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import requests
from pip._internal.utils.appdirs import user_cache_dir
from tqdm import tqdm

bucket_name = "tuttusa-raw"

main_data_path = pathlib.Path(user_cache_dir("tuttusa_raw"))
main_data_path.mkdir(parents=True, exist_ok=True)

import os
import boto3


def aws_session(region_name='us-east-1'):
    aws_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_key_secret = os.environ.get('AWS_ACCESS_KEY_SECRET')

    assert aws_key_id is not None, "AWS_ACCESS_KEY_ID must be set in environement path"
    assert aws_key_secret is not None, "AWS_ACCESS_KEY_SECRET must be set in environement path"

    return boto3.session.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                 aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET'),
                                 region_name=region_name)


def store_syth(data, name):
    path = main_data_path.joinpath(name).as_posix()
    with open(path, 'wb') as file:
        pickle.dump(data, file)
        file.close()


def load_synth(name):
    path = main_data_path.joinpath(name).as_posix()
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


def download_file(url, name):
    chunk_size = 1024
    r = requests.get(url, stream=True)
    pbar = tqdm(unit="B", total=int(r.headers['Content-Length']))
    path = main_data_path.joinpath(name).as_posix()
    with open(path, 'wb') as file:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:  # filter out keep-alive new chunks
                pbar.update(len(chunk))
                file.write(chunk)
        file.close()


def upload_data_to_cloud(data, name):
    session = aws_session()
    s3_resource = session.resource('s3')

    new_file, filename = tempfile.mkstemp()

    with open(filename, 'wb') as file:
        pickle.dump(data, file)
        file.close()

    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(Filename=filename, Key=name)


def download_data_from_cloud(name):
    u = f"https://{bucket_name}.s3.amazonaws.com/{name}"
    path = main_data_path.joinpath(name).as_posix()
    download_file(u, path)
    return load_synth(name)
