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

import numpy as np
from allennlp.common.util import JsonDict
from allennlp.data import Instance
from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_models.tagging.models import CrfTagger
from overrides import overrides

from seacorenlp.data.tokenizers import Tokenizer
from seacorenlp.tagging.pos.training.dataset_reader import UDPOSReader
from seacorenlp.tagging.pos.training.model import (
    POSLSTMTagger,
    POSTransformerTagger,
)


class POSPredictor(Predictor):
    def __init__(self, model_path: str, lang: str) -> None:
        archive = load_archive(model_path)
        super().__init__(archive.model, archive.dataset_reader)
        self._tokenizer = Tokenizer.from_default(lang)

    def predict(self, sentence: str) -> List[str]:
        tokens = [token.text for token in self._tokenizer.tokenize(sentence)]
        logits = self.predict_json({"sentence": sentence})["logits"]
        tag_ids = np.argmax(logits, axis=-1)
        pos_tags = [
            self._model.vocab.get_token_from_index(id, "labels")
            for id in tag_ids
        ]
        return list(zip(tokens, pos_tags))

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        tokens = self._tokenizer.tokenize(json_dict["sentence"])
        return self._dataset_reader.text_to_instance(tokens)
