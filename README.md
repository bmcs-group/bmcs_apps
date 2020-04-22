# bmcsapps

The repository contains a chain of jupyter notebooks explaining the basic
concepts in the modeling of bond and cracking behavior in brittle-matrix
composites. Jupyter notebooks serve as the top layer of numerical and 
semi-analytical models provided in the BMCS Tool Suite.

Each notebook contains a theoretical preamble which is accompanied 
by executable form of the derived formulae expressed within sympy package. 
Then, numerically executable functions are generated from the symbolic 
derivation. Large models, including nonlinear finite-element simulations
are realized with the help of numpy package. They serve as 
a basis for interactive execution of the model providedat 
the end of the notebooks
The interaction with the model is implemented using 
the ipywidget/matplotlib packages.

Prerequisites: The anaconda suite is required for installation. See a
minimum set of required packages in environment.yml file.

The entry point to the jupyter suite is the index.ipynb notebook.

The notebooks can be open also in the clouds without any local installation
using the binder service. It takes a while for the repository image to  
build up. 

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/rosoba/bmcsapps.git/master?filepath=index.ipynb)




