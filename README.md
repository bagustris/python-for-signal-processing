Jupyter notebooks for Python 3 (tested on 3.6 and 3.8) for Signal
Processing. This forked repository is a teaching material for 
the signal processing master course at Engineering Physics [ITS](https://www.its.ac.id).

Notebook Viewer Static Page Views
-----------------------------------

**Signal Processing Reading List**

- [Sampling Theorem Part_1](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Sampling_Theorem_Part_1.ipynb)
- [Sampling Theorem Part_2](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Sampling_Theorem_Part_2.ipynb)
- [Fourier Transform](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Fourier_Transform.ipynb)
- [Frequency Resolution](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Frequency_Resolution.ipynb)
- [More Fourier Transform](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/More_Fourier_Transform.ipynb)
- [Windowing Part1](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Windowing_Part1.ipynb)
- [Windowing Part2](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Windowing_Part2.ipynb)
- [Windowing Part3](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Windowing_Part3.ipynb)
- [Filtering Part1](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Filtering_Part1.ipynb)
- [Filtering Part2](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Filtering_Part2.ipynb)
- [Filtering Part3](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Filtering_Part3.ipynb)
- [Compressive Sampling](https://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Compressive_Sampling.ipynb)

**Stochastic Processes Reading List**

- [Conditional Expectation Gaussian](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Conditional_Expectation_Gaussian.ipynb)
- [Conditional expectation MSE](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Conditional_expectation_MSE.ipynb)
- [Conditional expectation MSE Ex](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Conditional_expectation_MSE_Ex.ipynb)
- [Conditional Expectation Projection](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Conditional_Expectation_Projection.ipynb)
- [Projection](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Projection.ipynb)
- [Projection Ex](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Projection_Ex.ipynb)
- [Projection mdim](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Projection_mdim.ipynb)
- [Inverse Projection Constrained Optimization](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Inverse_Projection_Constrained_Optimization.ipynb)
- [Gauss Markov](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Gauss_Markov.ipynb)
- [Maximum likelihood](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Maximum_likelihood.ipynb)
- [Expectation Maximization](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Expectation_Maximization.ipynb)
- [Markov chains](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Markov_chains.ipynb)
- [Buffons Needle Sim](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Buffons_Needle_Sim.ipynb)
- [Sampling Monte Carlo](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Sampling_Monte_Carlo.ipynb)
- [Rectangle Wedge Tail Decomposition](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Rectangle_Wedge_Tail_Decomposition.ipynb)

**Misc.**

- [Example CSVs](http://github.com/bagustris/python-for-signal-processing/blob/master/notebook/Example_CSVs.ipynb)

## How to build jupyter books 

```bash
uv venv .venv --python 3.12
uv pip install -r requirements.txt --python .venv/bin/python
.venv/bin/jupyter-book build . --path-output _build-jupyterbook

# (Optional) copy generated HTML into docs/ for local preview
rm -rf docs && mkdir -p docs && cp -a _build-jupyterbook/_build/html/. docs/
```