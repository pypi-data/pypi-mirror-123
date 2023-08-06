# pygmtools

### Overview

The pygmtools package is developed to fairly compare existing deep graph matching algorithms under different datasets & experiment settings. The pygmtools package provides a unified data interface and a evaluating platform for different datasets. Currently, pygmtools supports 5 datasets, including PascalVOC, Willow-Object, SPair-71k, CUB2011 and IMC-PT-SparseGM.



### Files

./

- dataset.py: The file includes 5 dataset classes, used to automatically download dataset and process the dataset into a json file, and also save train set and test set.

- benchmark.py: The file includes Benchmark class that can be used to fetch data from json file and evaluate prediction result.
- dataset_config.py: Fixed dataset settings, mostly dataset path and classes.



### Installation

Simple installation via Pip

```shell
pip install pygmtools
```



### Example

```python
from pygmtools.benchmark import Benchmark

# Define Benchmark on PascalVOC.
bm = Benchmark(name='PascalVOC', sets='train', 
               obj_resize=(256, 256), problem='2GM',
               filter='intersection')

# Random fetch data and ground truth.
data_list, gt_dict, _ = bm.rand_get_data(cls=None, num=2)
```

