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

from allennlp.common.util import JsonDict
from allennlp.data import Instance
from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_models.structured_prediction import (
    PennTreeBankConstituencySpanDatasetReader,
    SpanConstituencyParser,
)
from nltk import Tree
from overrides import overrides

from seacorenlp.data.tokenizers import SentenceSplitter, Tokenizer
from seacorenlp.tagging.pos import POSTagger


class ConstituencyParserPredictor(Predictor):
    VALID_LANGUAGES = {"id", "ms", "th", "vi"}
    VALID_POS_LANGUAGES = {"id", "ms", "th", "vi"}

    def __init__(
        self, model_path: str, lang: str, predict_pos: bool = False
    ) -> None:
        assert (
            lang in ConstituencyParserPredictor.VALID_LANGUAGES
        ), f"Language {lang} is not supported for tokenization."
        if predict_pos:
            assert (
                lang in ConstituencyParserPredictor.VALID_POS_LANGUAGES
            ), f"Language {lang} not supported for POS tagging. Set predict_pos to False."

        archive = load_archive(model_path)
        super().__init__(archive.model, archive.dataset_reader)
        self._dataset_reader._use_pos_tags = predict_pos
        self._tokenizer = Tokenizer.from_default(lang)
        self._sentence_splitter = SentenceSplitter.from_default(lang)
        self._pos_tagger = (
            POSTagger.from_default(lang) if predict_pos else None
        )

    def predict(self, text: str) -> List[Tree]:
        sentences = self._sentence_splitter.split_sentences(text)
        return [self.predict_json({"sentence": sent}) for sent in sentences]

    @overrides
    def predict_instance(self, instance: Instance) -> Tree:
        outputs = self._model.forward_on_instance(instance)
        return outputs["trees"]

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        tokens = self._tokenizer.tokenize(json_dict["sentence"])
        # Grab POS tag from word-POS tuples
        pos_tags = (
            [
                tuple[1]
                for tuple in self._pos_tagger.predict(json_dict["sentence"])
            ]
            if self._pos_tagger
            else None
        )
        return self._dataset_reader.text_to_instance(
            [token.text for token in tokens], pos_tags
        )
