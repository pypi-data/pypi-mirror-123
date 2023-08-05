# SEACoreNLP: A Python NLP Toolkit for Southeast Asian Languages

SEACoreNLP is an initiative by NLPHub of [AI Singapore] that aims to provide a one-stop solution for Natural Language Processing (NLP) in Southeast Asia.

It brings together the available open-source resources (be it datasets, models or libraries) and unifies them with a single framework. We also train models on available data whenever the opportunity arises and provide them through our package on top of the third-party libraries and models.

[AI Singapore]: https://aisingapore.org

## Demo

Please refer to our [demo] to see our models in action.

[demo]: https://seacorenlp.aisingapore.net

## Languages Supported

We currently support the following languages:

- Indonesian
- Thai
- Vietnamese

## Core NLP Tasks

The core NLP tasks that we cover are as follows:

- Word Tokenization
- Sentence Segmentation
- Part-of-speech Tagging (POS Tagging)
- Named Entity Recognition (NER)
- Constituency Parsing
- Dependency Parsing

## Installation

```shell
pip install seacorenlp
```

If you wish to make use of models from Stanza (one of the third-party libraries that we use), ensure that you also install the relevant models after installing `seacorenlp`.

```python
import stanza

stanza.download('id') # Download Indonesian models
stanza.download('vi') # Download Vietnamese models

# Stanza does not have models for Thai
```

As there are some dependency conflicts between the latest version of `underthesea` (a package for Vietnamese NLP that SEACoreNLP depends on) and the other packages used in SEACoreNLP, we are installing an earlier version (`1.2.3`) that does not have conflicts. However, this version does not contain the Vietnamese dependency parser, so if you wish to make use of that, please manually upgrade the version of `underthesea` to the latest version.

You may consider using our natively trained Vietnamese dependency parsers if you do not wish to perform this manual upgrade:

```python
from seacorenlp.parsing import DependencyParser

# Load best Vietnamese dependency parser trained on Universal Dependencies data
parser = DependencyParser.from_pretrained("dp-vi-ud-xlmr-best")
parser.predict("Tôi muốn ăn cơm.")
```

## Usage

We provide a command-line interface for training, evaluation and prediction. We also provide classes (such as `Tokenizer`, `POSTagger`, `NERTagger` etc.) and models that can be used in a manner reminiscent of Huggingface Transformers.

```python
from seacorenlp.tagging import POSTagger

th_text = 'ผมอยากกินข้าว'

# Native Models
native_tagger = POSTagger.from_pretrained('pos-th-ud-xlmr')
native_tagger.predict(th_text)
# Output: [('ผม', 'PRON'), ('อยาก', 'VERB'), ('กิน', 'VERB'), ('ข้าว', 'NOUN')]

# External Models
# Include keyword arguments as necessary (see respective class documentation)
external_tagger = POSTagger.from_library('pythainlp', corpus='orchid')
external_tagger.predict(th_text)
# Output: [('ผม', 'PPRS'), ('อยาก', 'XVMM'), ('กิน', 'VACT'), ('ข้าว', 'NCMN')]
```

Please refer to our [documentation] for details.

[documentation]: https://seacorenlp.aisingapore.net/docs
