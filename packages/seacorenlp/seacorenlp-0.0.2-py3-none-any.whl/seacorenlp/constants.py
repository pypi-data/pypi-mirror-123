import pathlib

# Paths
PACKAGE_ROOT = (pathlib.Path(__file__).parent).resolve()
TRAINING_CONFIG_FOLDER = PACKAGE_ROOT / "training_resources" / "config"
LOCAL_RESOURCES_FOLDER = (
    PACKAGE_ROOT / ".."
).resolve() / "seacorenlp_resources"
CLOUD_STORAGE_URL = "https://storage.googleapis.com/seacorenlp/models/"


# Tasks
TASKS = {"pos", "ner", "constituency", "dependency"}
MODEL_TASK_FOLDER = {
    "pos": "tagging/pos/",
    "ner": "tagging/ner/",
    "cp": "parsing/constituency/",
    "dp": "parsing/dependency/",
}


# Models
POS_MODELS = {
    "pos-id-ud-bilstm",
    "pos-id-ud-indobert",
    "pos-id-ud-xlmr",
    "pos-id-ud-xlmr-best",
    "pos-th-ud-bilstm",
    "pos-th-ud-bilstmcrf",
    "pos-th-ud-xlmr",
    "pos-th-ud-xlmr-best",
    "pos-vi-ud-bilstm",
    "pos-vi-ud-phobert",
    "pos-vi-ud-xlmr",
    "pos-vi-ud-xlmr-best",
}

NER_MODELS = {
    "ner-th-thainer-scratch",
    "ner-th-thainer-xlmr",
    "ner-th-thainer-xlmr-best",
    "ner-id-nergrit-xlmr",
    "ner-id-nergrit-xlmr-best",
}

CP_MODELS = {"cp-id-kethu-benepar-xlmr-best", "cp-id-kethu-xlmr"}

DP_MODELS = {
    "dp-id-ud-scratch",
    "dp-id-ud-indobert",
    "dp-id-ud-xlmr",
    "dp-id-ud-xlmr-best",
    "dp-th-ud-scratch",
    "dp-th-ud-xlmr",
    "dp-th-ud-xlmr-best",
    "dp-vi-ud-scratch",
    "dp-vi-ud-xlmr",
    "dp-vi-ud-xlmr-best",
}

AVAILABLE_MODELS = set().union(POS_MODELS, NER_MODELS, CP_MODELS, DP_MODELS)
