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
from allennlp.data.tokenizers.sentence_splitter import SentenceSplitter
from overrides import overrides


@SentenceSplitter.register("th")
class ThaiSentenceSplitter(SentenceSplitter):
    def __init__(self):
        self.splitter = pythainlp.tokenize.sent_tokenize

    @overrides
    def split_sentences(self, text: str) -> List[str]:
        """
        AllenNLP wrapper for PyThaiNLP sentence segmentation for Thai.
        Uses the 'crfcut' engine by default.
        """
        return self.splitter(text, keep_whitespace=False)


@SentenceSplitter.register("vi")
class VietnameseSentenceSplitter(SentenceSplitter):
    def __init__(self):
        self.splitter = underthesea.sent_tokenize

    @overrides
    def split_sentences(self, text: str) -> List[str]:
        """
        AllenNLP wrapper for UnderTheSea sentence segmentation for Vietnamese.
        """
        return self.splitter(text)
