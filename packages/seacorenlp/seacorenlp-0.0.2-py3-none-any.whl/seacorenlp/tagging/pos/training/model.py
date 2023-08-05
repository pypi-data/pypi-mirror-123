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
from typing import Dict

import torch
from allennlp.data import Vocabulary
from allennlp.models import Model
from allennlp.modules import Seq2SeqEncoder, TextFieldEmbedder
from allennlp.nn.util import (
    get_text_field_mask,
    sequence_cross_entropy_with_logits,
)
from allennlp.training.metrics import CategoricalAccuracy
from allennlp_models.tagging.models import CrfTagger


@Model.register("pos-lstm-tagger")
class POSLSTMTagger(Model):
    def __init__(
        self,
        vocab: Vocabulary,
        embeddings: TextFieldEmbedder,
        encoder: Seq2SeqEncoder,
    ):
        super().__init__(vocab)
        self.embeddings, self.encoder = embeddings, encoder
        num_labels = vocab.get_vocab_size("labels")
        self.tagger = torch.nn.Linear(encoder.get_output_dim(), num_labels)
        self.accuracy = CategoricalAccuracy()

    def forward(
        self, tokens: Dict[str, torch.Tensor], tags: torch.Tensor = None
    ) -> torch.Tensor:

        embedded_sentence = self.embeddings(tokens)
        mask = get_text_field_mask(tokens)
        encoded_sentence = self.encoder(embedded_sentence, mask)
        logits = self.tagger(encoded_sentence)

        output = {"logits": logits}
        if tags is not None:
            self.accuracy(logits, tags, mask)
            output["loss"] = sequence_cross_entropy_with_logits(
                logits, tags, mask
            )
        return output

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        return {"accuracy": self.accuracy.get_metric(reset)}


@Model.register("pos-transformer-tagger")
class POSTransformerTagger(Model):
    def __init__(self, vocab: Vocabulary, embeddings: TextFieldEmbedder):
        super().__init__(vocab)
        self.embeddings = embeddings
        num_labels = vocab.get_vocab_size("labels")
        self.tagger = torch.nn.Linear(embeddings.get_output_dim(), num_labels)
        self.accuracy = CategoricalAccuracy()

    def forward(
        self,
        tokens: Dict[str, torch.Tensor],
        tags: torch.Tensor = None,
        **args
    ) -> Dict[str, torch.Tensor]:

        embedded_sentence = self.embeddings(tokens)
        mask = get_text_field_mask(tokens)
        logits = self.tagger(embedded_sentence)

        output = {"logits": logits}

        if tags is not None:
            self.accuracy(logits, tags, mask)
            output["loss"] = sequence_cross_entropy_with_logits(
                logits, tags, mask
            )

        return output

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        return {"accuracy": self.accuracy.get_metric(reset)}
