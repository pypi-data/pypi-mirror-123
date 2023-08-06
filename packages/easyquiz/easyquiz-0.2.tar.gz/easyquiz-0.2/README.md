<p align="center">
<img src="./resources/eq_logo_plain.svg" alt="easyQuiz logo" width="400">
</p>

<h4 align="center">a multiple choice quiz creator for Jupyter notebooks</h4>

<p align="center">
  <a href="#Description">Description</a> -
  <a href="#Installation">Installation</a> - 
  <a href="#Usage"> Usage </a> -
  <a href="#Troubleshooting">Troubleshooting</a> -
  <a href="#License">License </a>
</p>



## Description


`easyquiz` is a simple package to create multiple choice questions for Jupyter notebook environments. It is designed to include formative evaluations within notebooks provided as class material.

Jupyter notebooks are a great resource to create interactive documents to be used as class material for engineerging education. However, non computer-related degree students usually lack programming experience and itis difficult to create engaggement with coding acitivies. easyQuiz  allow to create tradiional quizzes for formative evaluation of the most important conceps delivered using the notebook.


## Installation


### Jupyter Notebooks:

Using a virtual environment is encouraged. The package has been tested using both Conda and Python virtual environmets (virtualenv). 

1. Install with [`pip3`](https://pypi.org/project/easyquiz/0.1/) using Pypi
    + `$ pip3 install easyquiz`

2. Install with `pip3`
    + Download or clone this repository.
    + On a terminal or console prompt navigate to the base root of easyquiz
    + Install using `pip3`:
      + `$ pip3 install .`

### Google Colab:

When using Google Colab a virtual enrironment is not neccesary.

1. Install with [`pip3`](https://pypi.org/project/easyquiz/0.1/) using Pypi
    + `$ pip3 install easyquiz`

## Usage

Please see the notebook examples for detailed usage instructions and examples.

## Troubleshooting

If options are does not appear on quiz.show(), please try this: (see [source](https://stackoverflow.com/questions/36351109/ipython-notebook-ipywidgets-does-not-show))

1. For non conda or virtualenv: con a command promet type:
   `$ jupyter nbextension enable --py widgetsnbextension`
2. For non conda or virtualenv: con a command promet type:
   `$ jupyter nbextension enable --py --sys-prefix widgetsnbextension`

## License

MIT license


