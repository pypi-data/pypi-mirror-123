# Lightweight Hyperparameter Optimization 🚀
[![Pyversions](https://img.shields.io/pypi/pyversions/mle-hyperopt.svg?style=flat-square)](https://pypi.python.org/pypi/mle-hyperopt)
[![PyPI version](https://badge.fury.io/py/mle-hyperopt.svg)](https://badge.fury.io/py/mle-hyperopt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/mle-hyperopt/blob/main/examples/getting_started.ipynb)
<a href="docs/logo_transparent.png_2"><img src="docs/logo_transparent.png" width="200" align="right" /></a>

Simple and intuitive hyperparameter optimization API for your Machine Learning Experiments (MLE). This includes simple grid and random search as well as sequential model-based optimization (SMBO) and a set of more unorthodox search algorithms (multi-objective via `nevergrad` and a coordinate-wise search). Portable hyperparameter spaces are available for real, integer and categorical-valued variables. The search strategies assume that the underlying objective is minimized (multiple by -1 if this is not the case). For a quickstart checkout the [notebook blog](https://github.com/RobertTLange/mle-hyperopt/blob/main/examples/getting_started.ipynb).

## The API 🎮

```python
from mle_hyperopt import RandomSearch

# Instantiate random search class
strategy = RandomSearch(real={"lrate": {"begin": 0.1,
                                        "end": 0.5,
                                        "prior": "log-uniform"}},
                        integer={"batch_size": {"begin": 32,
                                                "end": 128,
                                                "prior": "uniform"}},
                        categorical={"arch": ["mlp", "cnn"]})

# Simple ask - eval - tell API
configs = strategy.ask(5)
values = [train_network(**c) for c in configs]
strategy.tell(configs, values)
```

### Implemented Search Types 	🔭

| Search Type           | Description | `search_config` |
|----------------------- | ----------- | --------------- |
|  `GridSearch`          |  Search over list of discrete values  | - |
|  `RandomSearch`        |  Random search over variable ranges         | `refine_after`, `refine_top_k` |
|  `SMBOSearch`          |  Sequential model-based optim.        | `base_estimator`, `acq_function`, `n_initial_points`
|  `CoordinateSearch`    |  Coordinate-wise optim. with defaults | `order`, `defaults`
|  `NevergradSearch`     |  Multi-objective [nevergrad](https://facebookresearch.github.io/nevergrad/) wrapper | `optimizer`, `budget_size`, `num_workers`

### Variable Types & Hyperparameter Spaces 🌍

| Variable            | Type | Space Specification |
|----------------------- | ----------- | --------------- |
|  **`real`**          |  Real-valued  | `Dict`: `begin`, `end`, `prior`/`bins` (grid) |
|  **`integer`**        |  Integer-valued         | `Dict`: `begin`, `end`, `prior`/`bins` (grid) |
|  **`categorical`**  |  Categorical        | `List`: Values to search over


## Installation ⏳

A PyPI installation is available via:

```
pip install mle-hyperopt
```

Alternatively, you can clone this repository and afterwards 'manually' install it:

```
git clone https://github.com/RobertTLange/mle-hyperopt.git
cd mle-hyperopt
pip install -e .
```

## Further Options 🚴

### Saving & Reloading Logs 🏪

```python
# Storing & reloading of results from .pkl
strategy.save("search_log.json")
strategy = RandomSearch(..., reload_path="search_log.json")

# Or manually add info after class instantiation
strategy = RandomSearch(...)
strategy.load("search_log.json")
```

### Search Decorator 🧶

```python
from mle_hyperopt import hyperopt

@hyperopt(strategy_type="grid",
          num_search_iters=25,
          real={"x": {"begin": 0., "end": 0.5, "bins": 5},
                "y": {"begin": 0, "end": 0.5, "bins": 5}})
def circle(config):
    distance = abs((config["x"] ** 2 + config["y"] ** 2))
    return distance

strategy = circle()
```

### Storing Configuration Files 📑


```python
# Store 2 proposed configurations - eval_0.yaml, eval_1.yaml
strategy.ask(2, store=True)
# Store with explicit configuration filenames - conf_0.yaml, conf_1.yaml
strategy.ask(2, store=True, config_fnames=["conf_0.yaml", "conf_1.yaml"])
```

### Retrieving Top Performers & Visualizing Results 📉

```python
# Get the top k best performing configurations
strategy.get_best(top_k=4)
```

### Refining the Search Space of Your Strategy 🪓

```python
# Refine the search space after 5 iterations based on top 2 configurations
strategy = RandomSearch(real={"lrate": {"begin": 0.1,
                                        "end": 0.5,
                                        "prior": "uniform"}},
                        integer={"batch_size": {"begin": 1,
                                                "end": 5,
                                                "prior": "log-uniform"}},
                        categorical={"arch": ["mlp", "cnn"]},
                        search_config={"refine_after": 5,
                                       "refine_top_k": 2})
```


## Development & Milestones for Next Release

You can run the test suite via `python -m pytest -vv tests/`. If you find a bug or are missing your favourite feature, feel free to contact me [@RobertTLange](https://twitter.com/RobertTLange) or create an issue :hugs:. Here are some features I want to implement for the next release:

- [ ] Add min vs max objective option to choose at strategy init
- [ ] Add text to notebook + visualization for what is implemented
- [ ] Allow space refinement for other strategies
