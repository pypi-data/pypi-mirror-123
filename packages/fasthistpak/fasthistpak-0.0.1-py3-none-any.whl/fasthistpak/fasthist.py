from typing import List, Tuple, Union
import numpy as np

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
    array = np.array(array)
    amin, amax = array.min(), array.max()
    bins_names = np.linspace(amin, amax, num=bins + 1, endpoint=True)
    value_counts = np.zeros(bins)
    bin_len = (amax - amin) / bins
    for x in array:
        index = int((x - amin) // bin_len)
        if (index == bins) or (index > 0 and bins_names[index] == x):
            index -= 1
        value_counts[index] += 1
    return value_counts, bins_names
