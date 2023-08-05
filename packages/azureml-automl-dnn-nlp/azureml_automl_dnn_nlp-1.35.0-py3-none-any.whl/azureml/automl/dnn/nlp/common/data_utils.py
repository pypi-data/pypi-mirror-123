# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Utils for reading input data."""

import logging
import os

from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.core import Dataset as AmlDataset
from azureml.data.abstract_dataset import AbstractDataset
from azureml.core.workspace import Workspace

_logger = logging.getLogger(__name__)


def get_dataset_by_id(
        dataset_id: str,
        dataset_type: str,
        workspace: Workspace
) -> AbstractDataset:
    """
    get dataset based on dataset id

    :param dataset_id: dataset id to retrieve
    :param dataset_type: dataset type label
    :param workspace: workspace to retrieve dataset from
    :return: dataset
    """
    Contract.assert_non_empty(
        dataset_id,
        dataset_type,
        reference_code=ReferenceCodes._DNN_NLP_EMPTY_DATASET_ID,
        log_safe=True
    )
    ds = AmlDataset.get_by_id(workspace, dataset_id)
    _logger.info("Fetched {}. Type: {}".format(dataset_type, type(ds)))
    return ds


def download_file_dataset(
        dataset_id: str,
        dataset_type: str,
        workspace: Workspace,
        ner_dir: str,
        overwrite: bool = False
) -> str:
    """
    load given dataset to data path and return the name of the file in reference

    :param dataset_id: dataset id to retrieve
    :param dataset_type: dataset type label
    :param workspace: workspace to retrieve dataset from
    :param ner_dir: directory where data should be downloaded
    :param overwrite: whether existing file can be overwritten
    :return: file name related to the dataset
    """
    _logger.info("Downloading file dataset for: {}".format(dataset_type))
    dataset = get_dataset_by_id(dataset_id, dataset_type, workspace)

    # to_path() returns format ["/filename.txt"], need to strip the "/"
    file_name = dataset.to_path()[0][1:]

    # Download data to ner_dir
    if not os.path.exists(ner_dir):
        os.makedirs(ner_dir)
    dataset.download(target_path=ner_dir, overwrite=overwrite)

    return file_name
