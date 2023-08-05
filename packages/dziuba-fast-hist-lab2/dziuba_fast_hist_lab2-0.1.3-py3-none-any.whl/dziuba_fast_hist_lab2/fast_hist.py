from typing import List, Tuple, Union
from collections import Counter
import random as rnd
#import matplotlib.pyplot as plt 
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
    max_elem = max(array)
    min_elem = min(array)
    delta = (max_elem - min_elem) / bins
    bins_names = np.arange(min_elem, max_elem, delta)
    bins_counts = np.zeros(bins)
    for val in array:
        idx = min(int((val - min_elem) / delta), bins - 1)
        bins_counts[idx] += 1
    return (np.array([int (x) for x in bins_counts]), bins_names)

# def test1():
#    """
#    Tests fast_hist on array [0.5, 0.5, 1.2, 6.5], bins = len(set(array))
#    """
#    array = [0.5, 0.5, 1.2, 6.5]
#    value_counts, bins_labels = fast_hist(array, len(set(array)))
#
#    plt.bar(bins_labels, value_counts, width = 0.7)

# def test2():
#     """
#   Tests fast_hist on array [1,1,2,3,4,1,2,3,4], bins = len(set(array))
#    """
#    array = [1,1,2,3,4,1,2,3,4]
#    value_counts, bins_labels = fast_hist(array, len(set(array)))
#
#    plt.bar(bins_labels, value_counts, width = 0.7)

#def test3():
#    """
#    Tests fast_hist on array of 50 random numbers in range 5000, bins = 100
#    """
#    rnd.seed(123)
#    array = [rnd.randint(0, 51) for _ in range(5000)]
#    value_counts, bins_labels = fast_hist(array, 100)
#
#    plt.bar(bins_labels, value_counts)

#def custom_test(array: List[Union[int, float]], bins: int):
#    """
#    Tests fast_hist on given array with given number of bins
#    """
#    value_counts, bins_labels = fast_hist(array, bins)
#
#    plt.bar(bins_labels, value_counts)
    
