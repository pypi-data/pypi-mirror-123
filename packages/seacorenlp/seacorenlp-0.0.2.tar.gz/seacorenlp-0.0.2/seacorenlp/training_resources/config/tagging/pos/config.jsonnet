# Variables
local train_data_path = std.extVar('train_data_path');
local validation_data_path = std.extVar('validation_data_path');

local use_pretrained = std.extVar('use_pretrained');
local model_name = std.extVar('model_name');
local freeze = std.extVar('freeze');
local train_parameters = if freeze == 'true' then false else true;

local embedding_dim = std.parseInt(std.extVar('embedding_dim'));
local hidden_dim = std.parseInt(std.extVar('hidden_dim'));

local num_epochs = std.parseInt(std.extVar('num_epochs'));
local patience = std.parseInt(std.extVar('patience'));
local batch_size = std.parseInt(std.extVar('batch_size'));
local lr = std.parseJson(std.extVar('lr'));

# Token indexers
local transformer_token_indexer(huggingface_name) = {
    "tokens": {
        "type": "pretrained_transformer_mismatched",
        "model_name": huggingface_name
    }
};

local single_id_token_indexer = {
    "tokens": {
        "type": "single_id"
    }
};

local token_indexers = {
    "bi-lstm": single_id_token_indexer,
    "bi-lstm-crf": single_id_token_indexer
};


# Model units
local bi_lstm_encoder = {
    "type": "lstm",
    "input_size": embedding_dim,
    "hidden_size": hidden_dim,
    "bidirectional": true
};

local bi_lstm_crf_model = {
    "type": "crf_tagger",
    "text_field_embedder": {
        "token_embedders": {
            "tokens": {
                "type": "embedding",
                "embedding_dim": embedding_dim
            }
        }
    },
    "encoder": bi_lstm_encoder
};

local bi_lstm_model = {
    "type": "pos-lstm-tagger",
    "embeddings": {
        "token_embedders": {
            "tokens": {
                "type": "embedding",
                "embedding_dim": embedding_dim
            }
        }
    },
    "encoder": bi_lstm_encoder
};

local transformer_model(huggingface_name) = {
    "type": "pos-transformer-tagger",
    "embeddings": {
        "token_embedders": {
            "tokens": {
                "type": "pretrained_transformer_mismatched",
                "model_name": huggingface_name,
                "train_parameters": train_parameters
            }
        }
    }
};

local models = {
    "bi-lstm": bi_lstm_model,
    "bi-lstm-crf": bi_lstm_crf_model
};

# Use use_pretrained flag to select indexers and embedders
local indexer = if use_pretrained == 'true' then transformer_token_indexer(model_name) else token_indexers[model_name];
local model = if use_pretrained == 'true' then transformer_model(model_name) else models[model_name];

# Config Template
{
    "dataset_reader" : {
        "type": "ud-pos-reader",
        "token_indexers": indexer
    },
    "train_data_path": train_data_path,
    "validation_data_path": validation_data_path,
    "model": model,
    "data_loader": {
        "batch_size": batch_size,
        "shuffle": true
    },
    "trainer": {
        "optimizer": {
            "type": "adam",
            "lr": lr
        },
        "num_epochs": num_epochs,
        "patience": patience
    }
}
