"""
Copyright (c) 2021 NLPHub AI Singapore

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import tarfile

import requests
from stanza.resources import common
from tqdm import tqdm

from seacorenlp.constants import (
    AVAILABLE_MODELS,
    CLOUD_STORAGE_URL,
    LOCAL_RESOURCES_FOLDER,
    MODEL_TASK_FOLDER,
)


def _check_if_model_is_valid(model_name: str) -> None:
    assert model_name in AVAILABLE_MODELS, (
        f"Model selected ({model_name}) is not available. "
        + "Please refer to our documentation to see which models are currently available."
    )


def _check_if_task_is_valid(model_task: str, class_task: str) -> None:
    assert (
        model_task == class_task
    ), "The model selected cannot be used with the class selected."


def _model_exists_in_local(model_name: str) -> bool:
    """
    Checks whether the model exists in local resources before downloading.
    Checks for either the existence of a folder (for Benepar models) or
    the existence of the gzip file itself (for other models).
    """
    file_path = LOCAL_RESOURCES_FOLDER / (model_name + ".tar.gz")
    folder_path = LOCAL_RESOURCES_FOLDER / model_name

    if not file_path.is_file() and not folder_path.is_dir():
        return False
    else:
        return True


def download_model(model_name: str) -> None:
    """
    Downloads a model from cloud storage based on its name.
    Model names are structured {task}-{language}-{dataset}-{embedding}.
    """

    task = model_name.split("-")[0]
    model_zip_name = model_name + ".tar.gz"
    url = CLOUD_STORAGE_URL + MODEL_TASK_FOLDER[task] + model_zip_name
    local_filepath = LOCAL_RESOURCES_FOLDER / model_zip_name

    if not LOCAL_RESOURCES_FOLDER.is_dir():
        LOCAL_RESOURCES_FOLDER.mkdir()

    r = requests.get(url, stream=True)
    with open(local_filepath, "wb") as f:
        file_size = int(r.headers.get("content-length"))
        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            desc=f"Downloading {model_name}...",
        ) as progress:
            for chunk in r.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    progress.update(len(chunk))
            progress.close()

    # Benepar models have to be run as a folder, not gzip file
    if task == "cp" and "benepar" in model_name:
        with tarfile.open(local_filepath) as zip_file:
            zip_file.extractall(path=LOCAL_RESOURCES_FOLDER)
            zip_file.close()
            os.remove(local_filepath)


def download_model_if_absent(model_name: str) -> None:
    if _model_exists_in_local(model_name):
        print(f"Loading {model_name} from local cache...")
    else:
        download_model(model_name)


def check_stanza_model_exists_in_local(
    lang: str, stanza_model_dir: str = common.DEFAULT_MODEL_DIR
) -> bool:
    """
    Raises exception if Stanza models are not found in the default folder
    and prompts user to download the model before proceeding. Returns True
    if the model folder has been found.
    """
    lang_model_path = os.path.join(stanza_model_dir, lang)
    if not (os.path.isdir(lang_model_path)):
        raise Exception(
            f"Stanza model for lang='{lang}' has not been downloaded, please do stanza.download('{lang}') before proceeding"
        )

    return True
