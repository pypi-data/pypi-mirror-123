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
from typing import List

import malaya
from allennlp.predictors import Predictor
from nltk.tree import Tree

from seacorenlp.data.tokenizers import SentenceSplitter

# This file contains a limited number of constituency parsers imported from external libraries.
# We currently only support Malay/Indonesian (Malaya).


class CustomConstituencyParser(Predictor):
    """An AllenNLP Predictor for Constituency Parsing using external libraries."""

    def __init__(self, lang: str) -> None:
        self.lang = lang
        self.sentence_splitter = SentenceSplitter.from_default(lang)
        self.parser = None

    def _predict_on_sentence(self, sentence: str) -> Tree:
        pass

    def predict(self, text: str) -> List[Tree]:
        sentences = self.sentence_splitter.split_sentences(text)
        return [self._predict_on_sentence(sent) for sent in sentences]


class IndonesianConstituencyParser(CustomConstituencyParser):
    """
    CustomConstituencyParser that calls Malaya's Constituency Parser module.

    Malaya's models were trained on an augmented Indonesian dataset and is
    therefore considered an Indonesian Constituency Parser (not Malay).
    """

    VALID_MODELS = {"bert", "tiny-bert", "albert", "tiny-albert", "xlnet"}

    def __init__(self, model: str = "xlnet", quantized: bool = False) -> None:
        assert (
            model in IndonesianConstituencyParser.VALID_MODELS
        ), f"Model name does not exist. Choose from {IndonesianConstituencyParser.VALID_MODELS}."
        super().__init__(lang="id")
        self.parser = malaya.constituency.transformer(
            model=model, quantized=quantized
        )

    def _predict_on_sentence(self, sentence: str) -> Tree:
        return self.parser.parse_nltk_tree(sentence)
