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

import stanza
import underthesea
from allennlp.data.tokenizers.token_class import Token
from allennlp.data.tokenizers.tokenizer import Tokenizer
from overrides import overrides
from stanza.models.common.doc import ID, MISC, TEXT, Document
from stanza.pipeline.processor import (
    ProcessorVariant,
    register_processor_variant,
)

from seacorenlp.utils import check_stanza_model_exists_in_local


@Tokenizer.register("stanza")
class StanzaTokenizer(Tokenizer):
    """
    A `Tokenizer` that uses stanza tokenizer. It will return allennlp Tokens and will not do sentence splitter.
    if sentence segmentation is needed, it should be implemented as `SentenceSplitter`.
    """

    def __init__(self, lang: str, **kwargs):
        check_stanza_model_exists_in_local(lang)

        self.stanza_tokenizer = stanza.Pipeline(
            lang=lang, processors="tokenize", tokenize_no_ssplit=True, **kwargs
        )

    @overrides
    def tokenize(self, text: str) -> List[Token]:
        stanza_doc = self.stanza_tokenizer(text)
        return [
            Token(text=token.text)
            for sentence in stanza_doc.sentences
            for token in sentence.tokens
        ]


@register_processor_variant("tokenize", "underthesea-tokenize")
class UnderTheSeaStanzaTokenizer(ProcessorVariant):
    """
    Stanza ProcessorVariant that tokenizes text using UnderTheSea tokenization engine.
    Mainly to replace the default Stanza Vietnamese tokenizer as it does not work well.
    """

    def __init__(self, config):
        pass

    def process(self, text: str) -> Document:
        sentences = underthesea.sent_tokenize(text)
        tokenized_sentences = [
            underthesea.word_tokenize(sent) for sent in sentences
        ]
        document = []
        idx = 0
        for sentence in tokenized_sentences:
            sent = []
            for token_id, token in enumerate(sentence):
                stanza_token = {
                    ID: (token_id + 1,),
                    TEXT: token,
                    MISC: f"start_char={idx}|end_char={idx + len(token)}",
                }
                sent.append(stanza_token)
                idx += len(token) + 1
            document.append(sent)
        return Document(document, text)
