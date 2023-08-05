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
from typing import Dict, Iterable, List

from allennlp.data import DatasetReader, Instance
from allennlp.data.fields import SequenceLabelField, TextField
from allennlp.data.token_indexers import SingleIdTokenIndexer, TokenIndexer
from allennlp.data.tokenizers import Token


@DatasetReader.register("ud-pos-reader")
class UDPOSReader(DatasetReader):
    """
    DatasetReader for reading POS data in UD CoNLL-U format.
    There are 10 fields for each token:
    ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
    E.g. "1	สำหรับ	_	ADP	IN	_	2	case	_	SpaceAfter=No"
    """

    def __init__(self, token_indexers: Dict[str, TokenIndexer] = None):
        super().__init__(lazy=False)
        self.token_indexers = token_indexers or {
            "tokens": SingleIdTokenIndexer()
        }

    def text_to_instance(
        self, tokens: List[Token], tags: List[str] = None
    ) -> Instance:
        sentence_field = TextField(tokens, self.token_indexers)
        fields = {"tokens": sentence_field}
        if tags:
            fields["tags"] = SequenceLabelField(
                labels=tags, sequence_field=sentence_field
            )
        return Instance(fields)

    def _read(self, file_path: str) -> Iterable[Instance]:
        raw_data = open(file_path, "r").read()
        entries = raw_data.split("\n\n")
        for entry in entries:
            # Remove comments containing sentence_id, text and translated text
            token_rows = [
                row for row in entry.split("\n") if row[0] is not "#"
            ]
            tokens = [Token(row.split("\t")[1]) for row in token_rows]
            tags = [row.split("\t")[3] for row in token_rows]
            yield self.text_to_instance(tokens, tags)
