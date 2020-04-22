# bmcsapps

## Focus
The repository contains a bundle of jupyter notebooks explaining the basic
concepts needed for modeling of bond and cracking behavior in brittle-matrix
composites. Applications are demonstrated on pullout tests and bending tests
of steel and carbon reinforced concrete composites that have been developed for
different types and scales of reinforcement bridging and pullout actions. 
Considered types of reinforcement include long, contiuous bars, textile fabrics, 
reinforcing sheets and short fiber. Jupyter notebooks serve as the top layer of numerical and 
semi-analytical models provided in the BMCS Tool Suite.

## Structure
Each notebook contains a theoretical preamble which is accompanied 
by executable form of the derived formulae expressed within sympy package. 
Then, numerically executable functions are generated from the symbolic 
derivation. Large models, including nonlinear finite-element simulations
are realized with the help of numpy package. They serve as a basis for interactive 
execution of the model provided at the end of the notebooks. The interaction 
with the model is implemented using the ipywidget/matplotlib packages.

## Prerequisites 
To execute the notebooks locally install the anaconda suite. Required packages
are specified in the environment.yml file. The entry point to the jupyter suite 
is the index.ipynb notebook.

## Binder
The notebooks can be open also in the clouds without any local installation
using the binder service. It takes a while for the repository image to build up.
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/rosoba/bmcsapps.git/master?filepath=index.ipynb)




