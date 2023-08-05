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
from allennlp.predictors import Predictor

from seacorenlp.constants import LOCAL_RESOURCES_FOLDER
from seacorenlp.utils import (
    _check_if_model_is_valid,
    _check_if_task_is_valid,
    download_model_if_absent,
)


class BasePredictor:
    TASK: str = ""
    PREDICTOR_CLASS: Predictor = None
    EXTERNAL_LIBRARIES: dict = {}
    DEFAULTS: dict = {}

    @classmethod
    def from_pretrained(cls, model_name: str) -> Predictor:
        """
        Returns a natively trained AllenNLP Predictor based on the model name provided

        Args:
            model_name: Name of the model
        """
        # 1. Check if model exists in our repository
        _check_if_model_is_valid(model_name)

        # 2. Check if task is appropriate for the class
        task, lang = model_name.split("-")[:2]
        _check_if_task_is_valid(task, cls.TASK)

        # 3. Check if model exists locally and download if necessary
        download_model_if_absent(model_name)

        model_path = LOCAL_RESOURCES_FOLDER / (model_name + ".tar.gz")

        return cls.PREDICTOR_CLASS(model_path, lang)

    @classmethod
    def from_library(cls, library_name: str, **kwargs) -> Predictor:
        """
        Returns a third-party Predictor based on the name of the library provided.

        Keyword arguments can be passed as necessary.

        Args:
            library_name: Name of third-party library
            **kwargs: Additional keyword arguments specific to each library
        """
        return cls.EXTERNAL_LIBRARIES[library_name](**kwargs)

    @classmethod
    def from_default(cls, lang: str) -> Predictor:
        """
        Returns a default Predictor based on the language specified.

        Args:
            lang: The 2-letter ISO 639-1 code of the desired language
        """
        if not cls.DEFAULTS:
            raise NotImplementedError(
                f"{cls.__name__} does not have default implementations."
            )

        config = cls.DEFAULTS.get(lang, None)
        if not config:
            raise ValueError(
                f"Language {lang} is not supported for {cls.__name__}."
            )
        return config["class"](**config["kwargs"])
