# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Score text dataset from model produced by training run."""

import argparse
import json
import logging
import os
import torch

from azureml.automl.dnn.nlp.classification.inference.multiclass_inferencer import MulticlassInferencer
from azureml.automl.dnn.nlp.common import utils
from azureml.automl.dnn.nlp.common.constants import (
    OutputLiterals,
    ScoringLiterals
)
from azureml.core.experiment import Experiment
from azureml.core.run import Run
from azureml.train.automl import constants


logger = logging.getLogger(__name__)


def _make_arg(arg_name: str) -> str:
    return "--{}".format(arg_name)


def _get_default_device():
    return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def _distill_run_from_experiment(run_id, experiment_name):
    """Obtain Run object from runId and experiment name

    :param run_id: azureml run id
    :type run_id: str
    :param experiment_name: name of experiment
    :type experiment_name: str
    :return: Run object
    :rtype: Run
    """
    current_experiment = Run.get_context().experiment
    experiment = current_experiment

    if experiment_name is not None:
        workspace = current_experiment.workspace
        experiment = Experiment(workspace, experiment_name)

    return Run(experiment=experiment, run_id=run_id)


def main():
    """Wrapper method to execute script only when called and not when imported."""
    parser = argparse.ArgumentParser()
    parser.add_argument(_make_arg(ScoringLiterals.RUN_ID),
                        help='run id of the experiment that generated the model')
    parser.add_argument(_make_arg(ScoringLiterals.EXPERIMENT_NAME),
                        help='experiment that ran the run which generated the model')
    parser.add_argument(_make_arg(ScoringLiterals.OUTPUT_FILE),
                        help='path to output file')
    parser.add_argument(_make_arg(ScoringLiterals.INPUT_DATASET_ID),
                        help='input_dataset_id')
    parser.add_argument(_make_arg(ScoringLiterals.LOG_OUTPUT_FILE_INFO),
                        help='log output file debug info', type=bool, default=False)

    args, unknown = parser.parse_known_args()

    task_type = constants.Tasks.TEXT_CLASSIFICATION
    utils._set_logging_parameters(task_type, args)

    device = _get_default_device()

    run_object = _distill_run_from_experiment(args.run_id, args.experiment_name)

    inferencer = MulticlassInferencer(run=run_object,
                                      device=device)

    label_column_name = json.loads(
        run_object.parent.parent.properties.get("AMLSettingsJsonString"))['label_column_name']
    featurization = json.loads(
        run_object.parent.parent.properties.get("AMLSettingsJsonString"))['featurization']

    dataset_language = utils._get_language_code(featurization)
    predicted_df = inferencer.score(args.input_dataset_id, label_column_name, dataset_language)

    os.makedirs(OutputLiterals.OUTPUT_DIR, exist_ok=True)
    predictions_path = os.path.join(OutputLiterals.OUTPUT_DIR, "predictions.csv")
    predicted_df.to_csv(predictions_path, index=False)
    logger.info("Results saved at location: {}".format(predictions_path))

    return


if __name__ == "__main__":
    # Execute only if run as a script
    main()
