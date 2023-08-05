"""
Module for segmentation tasks (word tokenization & sentence segmentation).
"""

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

from allennlp.data.tokenizers.sentence_splitter import SpacySentenceSplitter

from seacorenlp.data.tokenizers.custom_tokenizer import (
    ThaiTokenizer,
    VietnameseTokenizer,
)
from seacorenlp.data.tokenizers.sentence_splitter import (
    ThaiSentenceSplitter,
    VietnameseSentenceSplitter,
)
from seacorenlp.data.tokenizers.stanza_tokenizer import (
    StanzaTokenizer,
    UnderTheSeaStanzaTokenizer,
)
from seacorenlp.models import BaseSegmenter


class Tokenizer(BaseSegmenter):
    """
    Base class to instantiate specific tokenizer for language.

    **Options for library_name:**
      * ``stanza`` (For Indonesian and Vietnamese)
      * ``pythainlp`` (For Thai)
      * ``underthesea`` (For Vietnamese)

    **Defaults available for the following languages:**
      * ``id``: Indonesian
      * ``ms``: Malay
      * ``th``: Thai
      * ``vi``: Vietnamese
    """

    EXTERNAL_LIBRARIES = {
        "stanza": StanzaTokenizer,
        "pythainlp": ThaiTokenizer,
        "underthesea": VietnameseTokenizer,
    }
    DEFAULTS = {
        "id": {"class": StanzaTokenizer, "kwargs": {"lang": "id"}},
        "ms": {"class": StanzaTokenizer, "kwargs": {"lang": "id"}},
        "th": {"class": ThaiTokenizer, "kwargs": {}},
        "vi": {"class": VietnameseTokenizer, "kwargs": {}},
    }


class SentenceSplitter(BaseSegmenter):
    """
    Base class to instantiate specific sentence segmenter for language.

    **Options for library_name:**
      * ``pythainlp`` (For Thai)
      * ``underthesea`` (For Vietnamese)

    **Defaults available for the following languages:**
      * ``id``: Indonesian
      * ``ms``: Malay
      * ``th``: Thai
      * ``vi``: Vietnamese
    """

    EXTERNAL_LIBRARIES = {
        "pythainlp": ThaiSentenceSplitter,
        "underthesea": VietnameseSentenceSplitter,
    }
    DEFAULTS = {
        "id": {"class": SpacySentenceSplitter, "kwargs": {"rule_based": True}},
        "ms": {"class": SpacySentenceSplitter, "kwargs": {"rule_based": True}},
        "th": {"class": ThaiSentenceSplitter, "kwargs": {}},
        "vi": {"class": VietnameseSentenceSplitter, "kwargs": {}},
    }
