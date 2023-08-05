# Variables
local train_data_path = std.extVar('train_data_path');
local validation_data_path = std.extVar('validation_data_path');

local use_pretrained = std.extVar('use_pretrained');
local model_name = std.extVar('model_name');
local freeze = std.extVar('freeze');
local train_parameters = if freeze == 'true' then false else true;

local embedding_dim = std.parseInt(std.extVar('embedding_dim'));
local lstm_input_dim = std.parseInt(std.extVar('lstm_input_dim'));
local lstm_hidden_dim = std.parseInt(std.extVar('lstm_hidden_dim'));
local lstm_layers = std.parseInt(std.extVar('lstm_layers'));
local lstm_dropout = std.parseJson(std.extVar('lstm_dropout'));
local ff_hidden_dim = std.parseInt(std.extVar('ff_hidden_dim'));

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

# Use use_pretrained flag to select indexers and embedders
local embedder = if use_pretrained == 'true' then transformer_text_field_embedder(model_name) else non_pretrained_embedder;
local indexer = if use_pretrained == 'true' then transformer_token_indexer(model_name) else non_pretrained_indexer;

# Configuration
{
    "dataset_reader" : {
        "type": "ptb_trees",
        "token_indexers": indexer
    },
    "train_data_path": train_data_path,
    "validation_data_path": validation_data_path,
    "model": {
      "type": "constituency_parser",
      "text_field_embedder": embedder,
      "encoder": {
        "type": "lstm",
        "input_size": lstm_input_dim,
        "hidden_size": lstm_hidden_dim,
        "bidirectional": true,
        "num_layers": lstm_layers,
        "dropout": lstm_dropout
      },
      "span_extractor": {
        "type": "bidirectional_endpoint",
        "input_dim": lstm_hidden_dim*2
      },
      "feedforward": {
        "hidden_dims": ff_hidden_dim,
        "input_dim": lstm_hidden_dim*2,
        "num_layers": 1,
        "activations": "relu"
      }
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
        "num_epochs": num_epochs,
        "patience": patience
    }
}
