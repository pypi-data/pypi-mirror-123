"""
Module for Part-of-speech Tagging
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
from seacorenlp.tagging.pos.custom_tagger import (
    MalayPOSTagger,
    ThaiPOSTagger,
    VietnamesePOSTagger,
)
from seacorenlp.tagging.pos.stanza_tagger import StanzaPOSTagger
from seacorenlp.tagging.pos.training import POSPredictor


class POSTagger(BasePredictor):
    """
    Base class to instantiate specific POSTagger (AllenNLP Predictor)

    **Options for model_name:**
      * E.g. ``pos-th-ud-xlmr``
      * Refer to table containing POS Tagger performance for full list

    **Options for library_name:**
      * ``malaya`` (For Indonesian/Malay)
      * ``stanza`` (For Indonesian and Vietnamese)
      * ``pythainlp`` (For Thai)
      * ``underthesea`` (For Vietnamese)

    **Defaults available for the following languages:**
      * ``id``: Indonesian
      * ``ms``: Malay
      * ``th``: Thai
      * ``vi``: Vietnamese
    """

    TASK = "pos"
    PREDICTOR_CLASS = POSPredictor
    EXTERNAL_LIBRARIES = {
        "malaya": MalayPOSTagger,
        "pythainlp": ThaiPOSTagger,
        "stanza": StanzaPOSTagger,
        "underthesea": VietnamesePOSTagger,
    }
    DEFAULTS = {
        "id": {"class": StanzaPOSTagger, "kwargs": {"lang": "id"}},
        "ms": {"class": MalayPOSTagger, "kwargs": {}},
        "th": {"class": ThaiPOSTagger, "kwargs": {}},
        "vi": {"class": VietnamesePOSTagger, "kwargs": {}},
    }
