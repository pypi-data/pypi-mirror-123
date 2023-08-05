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
import underthesea
from allennlp.predictors import Predictor
from pythainlp.tag.named_entity import ThaiNameTagger


class CustomNERTagger(Predictor):
    def __init__(self, lang: str):
        self.lang = lang

    def predict(self, text: str) -> List[Tuple[str, str]]:
        pass


class ThaiNERTagger(CustomNERTagger):
    def __init__(self) -> None:
        """Use pythainlp to do named entity prediction.
        https://www.thainlp.org/pythainlp/docs/2.0/api/tag.html#pythainlp.tag.named_entity.ThaiNameTagger
        ThaiNameTagger has builtin tokenization in its method, so no tokenizer needed.
        """
        super().__init__(lang="th")
        self._model = ThaiNameTagger()

    def predict(self, text: str) -> List[Tuple[str, str]]:
        """Given text, output tuple of token and it's entity

        Args:
            text: sentence.

        Returns:
            List of Tuple[token, entity prediction]
        """
        return self._model.get_ner(text, pos=False)


class MalayNERTagger(CustomNERTagger):
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
        """Use malaya library to output named entity prediction.
        https://malaya.readthedocs.io/en/latest/load-entities.html?highlight=named%20entity%20recognition

        Args:
            model, one of [bert, tiny-bert, albert, tiny-albert, xlnet, alxlnet]
        """
        super().__init__(lang="ms")
        if model not in MalayNERTagger.VALID_MODELS:
            raise Exception(
                f"model name {model} should be in one of {MalayNERTagger.VALID_MODELS}"
            )

        self._model = malaya.entity.transformer(
            model=model, quantized=quantized
        )

    def _to_bio_format(
        self, predictions: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        reformatted = []
        if len(predictions) > 0:
            for i, (token, entity) in enumerate(predictions):
                reformatted_entity = "O"

                if entity != "OTHER":
                    prefix = "B"
                    # use naive solution, though this may be wrong
                    if i > 0 and predictions[i - 1][1] == entity:
                        prefix = "I"

                    reformatted_entity = f"{prefix}-{entity.upper()}"

                reformatted.append((token, reformatted_entity))

        return reformatted

    def predict(self, text: str, use_bio_format=True) -> List[Tuple[str, str]]:
        """Given text, output tuple of token and it's entity

        Args:
            text: sentence.
            use_bio_format: bool. Whether to use BIO format or return the standard entities supported by malaya
        Returns:
            List of Tuple[token, entity prediction]
        """
        original_predictions = self._model.predict(text)

        if use_bio_format:
            return self._to_bio_format(original_predictions)

        return original_predictions


class VietnameseNERTagger(CustomNERTagger):
    """
    NamedEntityPredictor based on the UnderTheSea library.
    https://underthesea.readthedocs.io/en/latest/readme.html#6-named-entity-recognition
    UnderTheSea has its own built-in tokenizer so no tokenizer is required here.
    """

    def __init__(self) -> None:
        super().__init__(lang="vi")
        self._model = underthesea.ner

    def predict(self, text: str) -> List[Tuple[str, str]]:
        predictions = self._model(
            text
        )  # Predictions in form of tuple (Token, POS, Chunk, Entity)
        sanitized_predictions = [
            (token[0], token[3]) for token in predictions
        ]  # Select Token and Entity from tuple
        return sanitized_predictions
