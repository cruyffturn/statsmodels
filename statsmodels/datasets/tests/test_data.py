import importlib

import numpy as np
import pandas as pd
import pytest

import statsmodels.datasets
from statsmodels.datasets.utils import Dataset

exclude = ['check_internet', 'clear_data_home', 'get_data_home',
           'get_rdataset', 'tests', 'utils', 'webuse']
datasets = []
for dataset_name in dir(statsmodels.datasets):
    if not dataset_name.startswith('_') and dataset_name not in exclude:
        datasets.append(dataset_name)


@pytest.mark.parametrize('dataset_name', datasets)
def test_dataset(dataset_name):
    dataset = importlib.import_module('statsmodels.datasets.' + dataset_name)

    ds = dataset.load()
    assert isinstance(ds, Dataset)
    assert isinstance(ds.data, np.recarray)
    if hasattr(ds, 'exog'):
        assert isinstance(ds.exog, np.ndarray)
    if hasattr(ds, 'endog'):
        assert isinstance(ds.endog, np.ndarray)

    ds2 = dataset.load_pandas()
    assert isinstance(ds2, Dataset)
    assert isinstance(ds2.data, pd.DataFrame)
    if hasattr(ds, 'exog'):
        assert isinstance(ds2.exog, (pd.DataFrame, pd.Series))
    if hasattr(ds, 'endog'):
        assert isinstance(ds2.endog, (pd.DataFrame, pd.Series))
