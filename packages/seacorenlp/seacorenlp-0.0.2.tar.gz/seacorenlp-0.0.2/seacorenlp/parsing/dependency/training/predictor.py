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

from allennlp.common.util import JsonDict
from allennlp.data import Instance
from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp_models.structured_prediction import (
    BiaffineDependencyParser,
    UniversalDependenciesDatasetReader,
)
from overrides import overrides

from seacorenlp.data.tokenizers import SentenceSplitter, Tokenizer
from seacorenlp.tagging import POSTagger


class DependencyParserPredictor(Predictor):
    VALID_LANGUAGES = {"id", "th", "vi", "ms"}

    def __init__(self, model_path: str, lang: str) -> None:
        assert (
            lang in DependencyParserPredictor.VALID_LANGUAGES
        ), f"Language {lang} is not supported for tokenization."

        archive = load_archive(model_path)
        super().__init__(archive.model, archive.dataset_reader)
        self._tokenizer = Tokenizer.from_default(lang)
        self._sentence_splitter = SentenceSplitter.from_default(lang)
        self._pos_tagger = POSTagger.from_default(lang)

    def predict(self, text: str) -> List[List[Tuple[str, int, str]]]:
        sentences = self._sentence_splitter.split_sentences(text)
        return [self.predict_json({"sentence": sent}) for sent in sentences]

    @overrides
    def predict_instance(
        self, instance: Instance
    ) -> List[Tuple[str, int, str]]:
        outputs = self._model.forward_on_instance(instance)

        # The models may sometimes predict a word as the root of a sentence
        # (head = 0) but still give it a dependency label that is not 'root'
        for i, head in enumerate(outputs["predicted_heads"]):
            if head == 0:
                outputs["predicted_dependencies"][i] = "root"

        # Convert from dictionary of lists to list of tuples
        sanitized_outputs = list(
            zip(
                outputs["words"],
                outputs["predicted_heads"],
                outputs["predicted_dependencies"],
            )
        )

        return sanitized_outputs

    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Instance:
        tokens = self._tokenizer.tokenize(json_dict["sentence"])
        # Grab POS tag from word-POS tuples
        pos_tags = [
            tuple[1]
            for tuple in self._pos_tagger.predict(json_dict["sentence"])
        ]

        return self._dataset_reader.text_to_instance(
            [token.text for token in tokens], pos_tags
        )
