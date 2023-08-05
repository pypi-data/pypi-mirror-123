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
from typing import List, Tuple

import malaya
import pythainlp
import underthesea
from allennlp.predictors import Predictor

from seacorenlp.data.tokenizers.custom_tokenizer import ThaiTokenizer

# This file contains a limited set of POS Taggers imported from external libraries
# We support only Thai (PyThaiNLP), Malay (Malaya) and Vietnamese (UnderTheSea) at the moment.


class CustomPOSTagger(Predictor):
    def __init__(
        self,
        lang: str,
        engine: str = None,
        corpus: str = None,
        tokenizer: str = None,
    ):
        self.lang = lang
        self.engine = engine
        self.corpus = corpus
        self.tokenizer = tokenizer

    def predict(self, text: str) -> List[Tuple[str, str]]:
        pass


class ThaiPOSTagger(CustomPOSTagger):
    """
    AllenNLP Predictor wrapped around PyThaiNLP's POS Tagger.
    Two models are available for use: Averaged Perceptron & Unigram Tagger
    """

    def __init__(
        self,
        engine: str = "perceptron",
        corpus: str = "orchid_ud",
        tokenizer: str = "attacut",
    ):
        """
        Initialize a PyThaiNLP POS Tagger, specifying the tokenizer, engine and training corpus.

        Tokenizer: Maximum Matching ('newmm') or Attacut ('attacut')
        Engine: Averaged Perceptron ('perceptron') or Unigram Tagger ('unigram') or RDRPOSTagger('artagger')
        Corpus: Orchid ('orchid'), Orchid UD ('orchid_ud'), Parallel UD ('pud') or LST20 ('lst20')
        """
        VALID_TOKENIZERS = {"newmm", "attacut"}
        VALID_ENGINES = {"perceptron", "unigram", "artagger"}
        VALID_CORPORA = {"orchid", "orchid_ud", "pud", "lst20"}
        assert (
            tokenizer in VALID_TOKENIZERS
        ), f"{tokenizer} is not a valid tokenizer."
        assert engine in VALID_ENGINES, f"{engine} is not a valid engine."
        assert corpus in VALID_CORPORA, f"{corpus} is not a valid corpus."

        super().__init__(
            lang="th", engine=engine, corpus=corpus, tokenizer=tokenizer
        )
        self.tokenizer = ThaiTokenizer(engine=tokenizer)

    def predict(self, text: str) -> List[Tuple[str, str]]:
        tokenized_text = [
            token.text for token in self.tokenizer.tokenize(text)
        ]
        return pythainlp.pos_tag(
            tokenized_text, engine=self.engine, corpus=self.corpus
        )


class MalayPOSTagger(CustomPOSTagger):
    """
    AllenNLP Predictor wrapped around Malaya's POS Tagger (BERT-based).
    """

    def __init__(self, engine: str = "alxlnet", quantized: bool = False):
        """
        Initialize a Malaya POS Tagger, specifying the BERT model to be used.

        Models: 'bert', 'tiny-bert', 'albert', 'tiny-albert', 'xlnet', 'alxlnet'
        """
        VALID_ENGINES = {
            "bert",
            "tiny-bert",
            "albert",
            "tiny-albert",
            "xlnet",
            "alxlnet",
        }
        assert engine in VALID_ENGINES, f"{engine} is not a valid engine."

        super().__init__(lang="ms", engine=engine)
        self.model = malaya.pos.transformer(model=engine, quantized=quantized)

    def predict(self, text: str) -> List[Tuple[str, str]]:
        return self.model.predict(text)


class VietnamesePOSTagger(CustomPOSTagger):
    """
    AllenNLP Predictor wrapped around UnderTheSea's POS Tagger. (CRF-based)
    """

    def __init__(self):
        super().__init__(lang="vi")

    def predict(self, text: str) -> List[Tuple[str, str]]:
        return underthesea.pos_tag(text)
