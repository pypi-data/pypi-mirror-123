# Variables
local train_data_path = std.extVar('train_data_path');
local validation_data_path = std.extVar('validation_data_path');
local dataset_reader = std.extVar('dataset_reader');

local use_pretrained = std.extVar('use_pretrained');
local model_name = std.extVar('model_name');
local freeze = std.extVar('freeze');
local train_parameters = if freeze == 'true' then false else true;
local transformer_hidden_dim = std.parseInt(std.extVar('transformer_hidden_dim'));

local embedding_dim = std.parseInt(std.extVar('embedding_dim'));
local use_char_embeddings = std.extVar('use_char_embeddings');
local char_embedding_dim = std.parseInt(std.extVar('char_embedding_dim'));
local ngram_filter_sizes = std.parseInt(std.extVar('ngram_filter_sizes'));
local num_filters = std.parseInt(std.extVar('num_filters'));
local char_cnn_dropout = std.parseJson(std.extVar('char_cnn_dropout'));

local lstm_hidden_dim = std.parseInt(std.extVar('lstm_hidden_dim'));
local lstm_layers = std.parseInt(std.extVar('lstm_layers'));
local lstm_dropout = std.parseJson(std.extVar('lstm_dropout'));

local num_epochs = std.parseInt(std.extVar('num_epochs'));
local patience = std.parseInt(std.extVar('patience'));
local batch_size = std.parseInt(std.extVar('batch_size'));
local lr = std.parseJson(std.extVar('lr'));


# Token Indexers
local non_pretrained_indexer = {
    "tokens": {
        "type": "single_id"
    }
};

local non_pretrained_indexer_with_char = {
    "tokens": {
        "type": "single_id"
    },
    "token_characters": {
        "type": "characters"
    }
};

local transformer_token_indexer(huggingface_name) = {
    "tokens": {
        "type": "pretrained_transformer_mismatched",
        "model_name": huggingface_name
    }
};

# Text Field Embedders
local non_pretrained_embedder = {
    "type": "basic",
    "token_embedders": {
        "tokens": {
            "type": "embedding",
            "embedding_dim": embedding_dim
        }
    }
};

local non_pretrained_embedder_with_char = {
    "type": "basic",
    "token_embedders": {
        "tokens": {
            "type": "embedding",
            "embedding_dim": embedding_dim
        },
        "token_characters": {
            "type": "character_encoding",
            "embedding": {
              "embedding_dim": char_embedding_dim
            },
            "encoder": {
                "type": "cnn",
                "embedding_dim": char_embedding_dim,
                "num_filters": num_filters,
                "ngram_filter_sizes": [ngram_filter_sizes]
              },
              "dropout": char_cnn_dropout
            }
    }
};

local transformer_text_field_embedder(huggingface_name) = {
    "type": "basic",
    "token_embedders": {
        "tokens": {
            "type": "pretrained_transformer_mismatched",
            "model_name": huggingface_name,
            "train_parameters": train_parameters
        }
    }
};

# Encoders
local lstm_input_size = if use_pretrained == 'true' then transformer_hidden_dim else if use_char_embeddings == 'true' then embedding_dim + num_filters else embedding_dim;

local bi_lstm_encoder = {
    "type": "lstm",
    "input_size": lstm_input_size,
    "hidden_size": lstm_hidden_dim,
    "bidirectional": true,
    "num_layers": lstm_layers,
    "dropout": lstm_dropout
};

# Use use_pretrained flag to select indexers and embedders
local indexer = if use_pretrained == 'true' then transformer_token_indexer(model_name) else if use_char_embeddings == 'true' then non_pretrained_indexer_with_char else non_pretrained_indexer;
local embedder = if use_pretrained == 'true' then transformer_text_field_embedder(model_name) else if use_char_embeddings == 'true' then non_pretrained_embedder_with_char else non_pretrained_embedder;

# Configuration
{
    "dataset_reader" : {
        "type": dataset_reader,
        "token_indexers": indexer
    },
    "train_data_path": train_data_path,
    "validation_data_path": validation_data_path,
    "model": {
      "type": "crf_tagger",
      "label_encoding": "BIO",
      "constrain_crf_decoding": true,
      "calculate_span_f1": true,
      "text_field_embedder": embedder,
      "encoder": bi_lstm_encoder
    },
    "data_loader": {
        "batch_size": batch_size,
        "shuffle": true
    },
    "trainer": {
        "optimizer": {
            "type": "adamw",
            "lr": lr
        },
        "validation_metric": "+f1-measure-overall",
        "num_epochs": num_epochs,
        "patience": patience
    }
}
