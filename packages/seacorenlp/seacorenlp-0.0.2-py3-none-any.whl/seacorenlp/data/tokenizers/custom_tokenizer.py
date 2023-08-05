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

import pythainlp
import underthesea
from allennlp.data.tokenizers.token_class import Token
from allennlp.data.tokenizers.tokenizer import Tokenizer
from overrides import overrides


class ThaiTokenizer(Tokenizer):
    VALID_TOKENIZER_ENGINE = {"attacut", "newmm"}
    """
    An AllenNLP tokenizer that makes use of PyThaiNLP's word tokenizing engine.
    Two options are available for the engine:
    'attacut': Default tokenizer. Good balance of accuracy and speed.
    'newmm': Dictionary-based, uses TCC and maximum matching, may produce longer tokens.
    """

    def __init__(self, engine: str = "attacut") -> None:
        if engine not in ThaiTokenizer.VALID_TOKENIZER_ENGINE:
            raise Exception(
                f"{engine} engine is not supported for Thai tokenizer!"
            )
        self.engine = engine

    @overrides
    def tokenize(self, text: str) -> List[Token]:
        words = pythainlp.tokenize.word_tokenize(text, engine=self.engine)
        return [Token(text=word) for word in words]


class VietnameseTokenizer(Tokenizer):
    """
    An AllenNLP Tokenizer for Vietnamese based on CRF using the UnderTheSea library.
    Does not perform sentence segmentation. Only feed in single sentences for best performance.
    """

    @overrides
    def tokenize(self, text: str) -> List[Token]:
        tokenized_text = underthesea.word_tokenize(text)
        return [Token(text=word) for word in tokenized_text]
