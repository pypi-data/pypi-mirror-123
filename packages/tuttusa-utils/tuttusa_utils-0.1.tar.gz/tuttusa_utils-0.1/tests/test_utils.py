#!/usr/bin/env python
"""Tests for `tuttusa_utils` package."""
# pylint: disable=redefined-outer-name

import pytest
import numpy as np
from tuttusa_utils.tuttusa_utils import store_syth, load_synth, upload_data_to_cloud, download_data_from_cloud


@pytest.fixture
def fake_data():
    return np.random.uniform(0, 1, (20, 30))


def test_store_load_locally(fake_data):
    """can store and load synthetic data locally"""

    store_syth(fake_data, "fake_data_test")

    n_fake_data = load_synth("fake_data_test")

    assert (n_fake_data == fake_data).all()


@pytest.mark.skip(reason="no way of currently testing this")
def test_store_load_cloud(fake_data):
    """can store and load synthetic data to the cloud"""
    upload_data_to_cloud(fake_data, "fake_data_test")

    n_fake_data = download_data_from_cloud("fake_data_test")

    assert (n_fake_data == fake_data).all()
