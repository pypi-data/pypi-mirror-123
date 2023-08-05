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

import stanza
from allennlp.predictors import Predictor
from stanza.models.common.doc import Document

from seacorenlp.utils import check_stanza_model_exists_in_local


@Predictor.register("stanza-pos-tagger")
class StanzaPOSTagger(Predictor):
    """An AllenNLP Predictor that makes use of Stanza POS taggers."""

    VALID_LANGUAGES = {"id", "ta", "vi"}

    def __init__(self, lang: str, **kwargs):
        check_stanza_model_exists_in_local(lang)

        assert (
            lang in StanzaPOSTagger.VALID_LANGUAGES
        ), f"Language {lang} not supported for Stanza POS Tagging!"

        if lang == "vi":
            # Replace default Stanza Vietnamese tokenizer with UnderTheSea's
            # as it does not work well especially with longer sentences.
            processors = {"tokenize": "underthesea-tokenize"}
        else:
            processors = "tokenize, pos"

        self.nlp = stanza.Pipeline(
            lang=lang, processors=processors, tokenize_no_ssplit=True, **kwargs
        )

    def _extract_pos_from_stanza_doc(
        self, doc: Document
    ) -> List[Tuple[str, str]]:
        pos_tags = [
            (word.text, word.upos)
            for sent in doc.sentences
            for word in sent.words
        ]
        return pos_tags

    def predict(self, text: str) -> List[Tuple[str, str]]:
        doc = self.nlp(text)
        pos_tags = self._extract_pos_from_stanza_doc(doc)
        return pos_tags
