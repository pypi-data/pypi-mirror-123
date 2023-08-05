# Variables
local train_data_path = std.extVar('train_data_path');
local validation_data_path = std.extVar('validation_data_path');

local use_pretrained = std.extVar('use_pretrained');
local model_name = std.extVar('model_name');
local freeze = std.extVar('freeze');
local train_parameters = if freeze == 'true' then false else true;

local embedding_dim = std.parseInt(std.extVar('embedding_dim'));
local pos_tag_embedding_dim = std.parseInt(std.extVar('pos_tag_embedding_dim'));

local lstm_input_dim = std.parseInt(std.extVar('lstm_input_dim'));
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



{
    "dataset_reader":{
        "type":"universal_dependencies",
        "token_indexers": indexer
    },
    "train_data_path": train_data_path,
    "validation_data_path": validation_data_path,
    "model": {
      "type": "biaffine_parser",
      "text_field_embedder": embedder,
      "pos_tag_embedding":{
        "embedding_dim": pos_tag_embedding_dim,
        "vocab_namespace": "pos",
        "sparse": true
      },
      "encoder": {
        "type": "stacked_bidirectional_lstm",
        "input_size": lstm_input_dim,
        "hidden_size": lstm_hidden_dim,
        "num_layers": lstm_layers,
        "recurrent_dropout_probability": lstm_dropout,
        "use_highway": true
      },
      "use_mst_decoding_for_validation": true,
      "arc_representation_dim": 500,
      "tag_representation_dim": 100,
      "dropout": 0.3,
      "input_dropout": 0.3,
      "initializer": {
        "regexes": [
          [".*projection.*weight", {"type": "xavier_uniform"}],
          [".*projection.*bias", {"type": "zero"}],
          [".*tag_bilinear.*weight", {"type": "xavier_uniform"}],
          [".*tag_bilinear.*bias", {"type": "zero"}],
          [".*weight_ih.*", {"type": "xavier_uniform"}],
          [".*weight_hh.*", {"type": "orthogonal"}],
          [".*bias_ih.*", {"type": "zero"}],
          [".*bias_hh.*", {"type": "lstm_hidden_bias"}]
        ]
      }
    },
    "data_loader": {
      "batch_sampler": {
        "type": "bucket",
        "batch_size" : batch_size
      }
    },
    "trainer": {
      "num_epochs": num_epochs,
      "grad_norm": 5.0,
      "patience": patience,
      "validation_metric": "+LAS",
      "optimizer": {
        "type": "dense_sparse_adam",
        "betas": [0.9, 0.9],
        "lr": lr
      }
    }
}
