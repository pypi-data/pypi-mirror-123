import numpy as np
import pandas as pd


def assert_frame_equal(left: pd.DataFrame, right: pd.DataFrame, sort_keys=None):
    if sort_keys is None:
        sort_keys = []
    if len(sort_keys):
        left = left.sort_values(by=sort_keys).reset_index(drop=True)
        right = right.sort_values(by=sort_keys).reset_index(drop=True)

    # pandas <= 1.1.5(<=python3.6) will throw 'left is not an ExtensionArray' when assert_frame_equal
    # pd.testing.assert_frame_equal(left, right, check_dtype=False, check_index_type=False)
    np.testing.assert_array_equal(left.values, right.values)
