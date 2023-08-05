"""
Module for Constituency Parsing
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

from typing import Union

from seacorenlp.constants import LOCAL_RESOURCES_FOLDER
from seacorenlp.models import BasePredictor
from seacorenlp.parsing.constituency.benepar_parser import (
    BeneparConstituencyParser,
)
from seacorenlp.parsing.constituency.custom_parser import (
    IndonesianConstituencyParser,
)
from seacorenlp.parsing.constituency.training import (
    ConstituencyParserPredictor,
)
from seacorenlp.utils import (
    _check_if_model_is_valid,
    _check_if_task_is_valid,
    download_model_if_absent,
)


class ConstituencyParser(BasePredictor):
    """
    Base class to instantiate specific ConstituencyParser (AllenNLP Predictor)

    **Options for model_name:**
      * E.g. ``cp-id-kethu-xlmr``
      * Refer to table containing Constituency Parser performance for full list

    **Options for library_name:**
      * ``malaya`` (For Indonesian/Malay)
    """

    TASK = "cp"
    EXTERNAL_LIBRARIES = {"malaya": IndonesianConstituencyParser}

    @classmethod
    def from_pretrained(
        cls, model_name: str
    ) -> Union[BeneparConstituencyParser, ConstituencyParserPredictor]:
        """
        Returns a natively trained ConstituencyParser based on the model name provided

        Args:
            model_name (str): Name of the model

        Returns:
            Predictor: An AllenNLP Predictor that performs constituency parsing
        """
        _check_if_model_is_valid(model_name)
        task, lang = model_name.split("-")[:2]
        _check_if_task_is_valid(task, cls.TASK)
        download_model_if_absent(model_name)

        if "benepar" in model_name:
            model_path = LOCAL_RESOURCES_FOLDER / model_name
            return BeneparConstituencyParser(str(model_path), lang)
        else:
            model_path = LOCAL_RESOURCES_FOLDER / (model_name + ".tar.gz")
            return ConstituencyParserPredictor(model_path, lang)
