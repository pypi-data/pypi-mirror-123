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

from allennlp.predictors import Predictor
from benepar import Parser
from nltk.tree import Tree

from seacorenlp.data.tokenizers import SentenceSplitter, Tokenizer


class BeneparConstituencyParser(Predictor):
    def __init__(self, model_path: str, lang: str) -> None:
        self.parser = Parser(model_path)
        self.lang = lang
        self._tokenizer = Tokenizer.from_default(lang)
        self._sentence_splitter = SentenceSplitter.from_default(lang)

    def predict(self, text: str) -> List[Tree]:
        sentences = self._sentence_splitter.split_sentences(text)
        tokenized_sentences = [
            [token.text for token in self._tokenizer.tokenize(sent)]
            for sent in sentences
        ]
        return [self.parser.parse(sent) for sent in tokenized_sentences]
