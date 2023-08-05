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
from argparse import ArgumentParser, Namespace

from allennlp.commands.evaluate import evaluate_from_args
from allennlp.commands.predict import _predict
from allennlp.commands.train import train_model_from_args
from allennlp.common.util import import_module_and_submodules

from seacorenlp.constants import TASKS, TRAINING_CONFIG_FOLDER


def get_module_for_task(args: Namespace) -> None:
    """
    Selects the relevant folders containing dataset readers
    and models for the training/evaluation of models and
    imports them.

    Args:
        args (Namespace): Arguments parsed from the command line
    """
    assert args.task in {
        "pos",
        "ner",
        "constituency",
        "dependency",
    }, f"{args.task} is not a supported task. Choose from {TASKS}."

    module = "seacorenlp"
    if args.task == "pos":
        module += ".tagging.pos.training"
    elif args.task == "ner":
        module += ".tagging.ner"
    elif args.task == "constituency":
        module += ".parsing.constituency.training"
    elif args.task == "dependency":
        module += ".parsing.dependency.training"

    return module


def add_training_config(args: Namespace) -> None:
    if args.task in {"pos", "ner"}:
        subdir = "tagging"
    elif args.task in {"constituency", "dependency"}:
        subdir = "parsing"
    args.param_path = (
        f"{TRAINING_CONFIG_FOLDER}/{subdir}/{args.task}/config.jsonnet"
    )


def train(args: Namespace) -> None:
    module = get_module_for_task(args)
    import_module_and_submodules(module)
    args.include_package = module
    add_training_config(args)
    train_model_from_args(args)


def evaluate(args: Namespace) -> None:
    module = get_module_for_task(args)
    import_module_and_submodules(module)
    metrics = evaluate_from_args(args)
    print(metrics)


def predict(args: Namespace) -> None:
    module = get_module_for_task(args)
    import_module_and_submodules(module)
    args.include_package = module
    _predict(args)


def main() -> None:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    subparser_train = subparsers.add_parser("train")
    subparser_train.set_defaults(callback=train)

    train_arguments_dict = {
        "--task": None,
        "--param-path": None,
        "--include-package": None,
        "--serialization-dir": "outputs",
        "--recover": False,
        "--force": None,
        "--overrides": "",
        "--node-rank": 0,
        "--dry-run": None,
        "--file-friendly-logging": False,
    }
    for arg, default in train_arguments_dict.items():
        subparser_train.add_argument(arg, default=default)

    subparser_eval = subparsers.add_parser("evaluate")
    subparser_eval.set_defaults(callback=evaluate)

    eval_arguments_dict = {
        "--task": None,
        "--archive_file": None,
        "--input_file": None,
        "--output-file": None,
        "--predictions-output-file": None,
        "--weights-file": None,
        "--batch-weight-key": "",
        "--batch-size": None,
        "--embedding-sources-mapping": "",
        "--extend-vocab": False,
        "--cuda_device": -1,
        "--overrides": "",
        "--file-friendly-logging": False,
    }
    for arg, default in eval_arguments_dict.items():
        subparser_eval.add_argument(arg, default=default)

    subparser_pred = subparsers.add_parser("predict")
    subparser_pred.set_defaults(callback=predict)

    pred_arguments_dict = {
        "--task": None,
        "--archive_file": None,
        "--input_file": None,
        "--output-file": None,
        "--use-dataset-reader": True,
        "--weights-file": None,
        "--silent": True,
        "--cuda-device": -1,
        "--batch-size": 1,
        "--overrides": "",
        "--predictor": None,
        "--predictor-args": "",
        "--multitask-head": None,
        "--dataset_reader_choice": "validation",
        "--file-friendly-logging": False,
    }
    for arg, default in pred_arguments_dict.items():
        subparser_pred.add_argument(arg, default=default)

    args = parser.parse_args()
    assert (
        args.task is not None
    ), f"Task must be specified. Available tasks: {TASKS}."

    args.callback(args)


if __name__ == "__main__":
    main()
