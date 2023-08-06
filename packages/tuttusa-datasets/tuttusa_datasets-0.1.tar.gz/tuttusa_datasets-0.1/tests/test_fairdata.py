#!/usr/bin/env python
"""Tests for `tuttusa_datasets` package."""
# pylint: disable=redefined-outer-name
from collections import OrderedDict

import pytest

from tuttusa_datasets.models import DataConfig, Dataset
from tuttusa_datasets.synthetic_data import GenerateData


@pytest.fixture
def data_config():
    return DataConfig(proportion=OrderedDict({"white": 0.3, "black": 0.3, "hispanic": 0.4}),
                      correlation=0.5,
                      disp=[0.0, 100.0, 200.0],  # normal situation,
                      noise_rate=0.2,
                      shuffle_noise=0.1,
                      use_name_proxy=False,
                      name="name_2",
                      process_proxy=True,
                      model_name="white_black_hispanic",
                      base_y_val=200,
                      t_labels=["white", "black", "hispanic"])


def test_generate_synth_dataset(data_config):
    dataset = GenerateData().regression_data(data_config, plot=False)

    assert isinstance(dataset, Dataset)
