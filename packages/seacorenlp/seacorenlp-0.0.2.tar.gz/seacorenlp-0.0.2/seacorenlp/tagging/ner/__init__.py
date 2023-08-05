"""
Module for Named Entity Recognition
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

from seacorenlp.models import BasePredictor
from seacorenlp.tagging.ner.custom_tagger import (
    MalayNERTagger,
    ThaiNERTagger,
    VietnameseNERTagger,
)
from seacorenlp.tagging.ner.training import NERPredictor


class NERTagger(BasePredictor):
    """
    Base class to instantiate specific NERTagger (AllenNLP Predictor)

    **Options for model_name:**
      * E.g. ``ner-th-thainer-xlmr``
      * Refer to table containing NER Tagger performance for full list

    **Options for library_name:**
      * ``malaya`` (For Indonesian/Malay)
      * ``pythainlp`` (For Thai)
      * ``underthesea`` (For Vietnamese)
    """

    TASK = "ner"
    PREDICTOR_CLASS = NERPredictor
    EXTERNAL_LIBRARIES = {
        "malaya": MalayNERTagger,
        "underthesea": VietnameseNERTagger,
        "pythainlp": ThaiNERTagger,
    }
