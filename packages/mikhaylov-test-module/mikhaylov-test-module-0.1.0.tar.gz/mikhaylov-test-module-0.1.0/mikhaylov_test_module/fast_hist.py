import numpy as np
from typing import List, Tuple, Union
from bisect import bisect


def fast_hist(array: List[Union[int, float]],
              bins: int) -> Tuple[List[int], List[float]]:
    """
    Builds bins' labels and bins' value counts for given array
    :param array: array with numeric values
    :param bins:  number of bins in result distribution
    :return: Two lists: 
             first contains value counts of each bin,
             second contains list of bins' labels
    """
    if len(array) == 0:
        return ([], [])
    labels = np.linspace(min(array), max(array), num=bins + 1)
    result = [0 for _ in range(bins)]
    for x in array:
        result[min(bisect(labels, x) - 1, len(result) - 1)] += 1
    return (result, labels.tolist())
