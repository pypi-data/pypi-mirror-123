"""
Module for Dependency Parsing
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
from seacorenlp.parsing.dependency.custom_parser import (
    IndonesianDependencyParser,
    ThaiDependencyParser,
    VietnameseDependencyParser,
)
from seacorenlp.parsing.dependency.training import DependencyParserPredictor


class DependencyParser(BasePredictor):
    """
    Base class to instantiate specific DependencyParser (AllenNLP Predictor)

    **Options for model_name:**
      * E.g. ``dp-th-ud-xlmr``
      * Refer to table containing Dependency Parser performance for full list

    **Options for library_name:**
      * ``malaya`` (For Indonesian/Malay)
      * ``pythainlp`` (For Thai)
      * ``underthesea`` (For Vietnamese)
    """

    TASK = "dp"
    PREDICTOR_CLASS = DependencyParserPredictor
    EXTERNAL_LIBRARIES = {
        "malaya": IndonesianDependencyParser,
        "pythainlp": ThaiDependencyParser,
        "underthesea": VietnameseDependencyParser,
    }
