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
from typing import List, Tuple

import malaya
import spacy_thai
import underthesea
from allennlp.predictors import Predictor

from seacorenlp.data.tokenizers import SentenceSplitter

# This file contains a limited number of dependency parser imported from external libraries.
# We currently support Thai (spaCy-Thai), Indonesian (Malaya) and Vietnamese (UnderTheSea).


class CustomDependencyParser(Predictor):
    def __init__(self, lang: str) -> None:
        self.lang = lang
        self.sentence_splitter = SentenceSplitter.from_default(lang)
        self.parser = None

    def _predict_on_sentence(self, text: str) -> List[Tuple[str, int, str]]:
        pass

    def predict(self, text: str) -> List[List[Tuple[str, int, str]]]:
        sentences = self.sentence_splitter.split_sentences(text)
        return [self._predict_on_sentence(sent) for sent in sentences]


class VietnameseDependencyParser(CustomDependencyParser):
    def __init__(self) -> None:
        super().__init__(lang="vi")
        self.parser = underthesea.dependency_parse

    def _predict_on_sentence(self, text: str) -> List[Tuple[str, int, str]]:
        return self.parser(text)


class ThaiDependencyParser(CustomDependencyParser):
    def __init__(self) -> None:
        super().__init__(lang="th")
        self.parser = spacy_thai.load()

    def _predict_on_sentence(self, text: str) -> List[Tuple[str, int, str]]:
        spacy_doc = self.parser(text)

        # Extract FORM, HEAD and DEPREL from spaCy Doc
        # ROOT should have 0 as its HEAD
        dependency_triplets = [
            (token.text, token.head.i + 1, token.dep_)
            if token.dep_ != "ROOT"
            else (token.text, 0, token.dep_)
            for token in spacy_doc
        ]

        return dependency_triplets


class IndonesianDependencyParser(CustomDependencyParser):
    VALID_MODELS = {
        "bert",
        "tiny-bert",
        "albert",
        "tiny-albert",
        "xlnet",
        "alxlnet",
    }

    def __init__(
        self, model: str = "alxlnet", quantized: bool = False
    ) -> None:
        assert (
            model in IndonesianDependencyParser.VALID_MODELS
        ), f"Model name does not exist. Choose from {IndonesianDependencyParser.VALID_MODELS}."

        super().__init__(lang="ms")
        self.parser = malaya.dependency.transformer(
            model=model, quantized=quantized
        )

    def _predict_on_sentence(self, text: str) -> List[Tuple[str, int, str]]:
        # Malaya's dependency parser return 3 things:
        # A dependency graph, tuples of DEPRELs and tuples of HEADs
        _, dep_tuples, head_tuples = self.parser.predict(text)

        dependency_triplets = [
            head_tuple + (dep_tuples[i][1],)
            for i, head_tuple in enumerate(head_tuples)
        ]

        return dependency_triplets
