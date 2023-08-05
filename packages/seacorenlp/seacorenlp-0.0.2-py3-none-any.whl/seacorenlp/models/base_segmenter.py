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
from typing import Union

from allennlp.data.tokenizers.sentence_splitter import SentenceSplitter
from allennlp.data.tokenizers.tokenizer import Tokenizer


class BaseSegmenter:
    EXTERNAL_LIBRARIES: dict = {}
    DEFAULTS: dict = {}

    @classmethod
    def from_library(
        cls, library_name: str, **kwargs
    ) -> Union[Tokenizer, SentenceSplitter]:
        """
        Returns a third-party segmenter based on the name of the library provided.

        Keyword arguments can be passed as necessary to specify the corpora and
        engines etc. for the third-party segmenter.

        Args:
            library_name: Name of third-party library
            **kwargs: Additional keyword arguments specific to each library
        """
        assert (
            library_name in cls.EXTERNAL_LIBRARIES.keys()
        ), f"{library_name} is not a valid library name."
        return cls.EXTERNAL_LIBRARIES[library_name](**kwargs)

    @classmethod
    def from_default(cls, lang: str) -> Union[Tokenizer, SentenceSplitter]:
        """
        Returns a default segmenter based on the language specified.

        Args:
            lang: The 2-letter ISO 639-1 code of the desired language
        """
        config = cls.DEFAULTS.get(lang, None)
        if not config:
            raise ValueError(
                f"Language {lang} is not supported for segmentation."
            )
        return config["class"](**config["kwargs"])
