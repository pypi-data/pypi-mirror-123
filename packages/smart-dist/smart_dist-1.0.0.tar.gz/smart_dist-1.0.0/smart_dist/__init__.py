from .Gaussiandistribution import Gaussian
from .Binomialdistribution import Binomial
from .Coinanalysis import crypto


"""
If you want to try using virtual environments in this workspace first, follow these instructions:

1. There is an issue with the Ubuntu operating system and Python3, in which the venv package isn't installed correctly. In the workspace, one way to fix this is by running this command in the workspace terminal: conda update python. For more information, see venv doesn't create activate script python3. Then, enter y when prompted. It might take a few minutes for the workspace to update. If you are not using Anaconda on your local computer, you can skip this first step.

2. Enter the following command to create a virtual environment: python -m venv venv_name where venv_name is the name you want to give to your virtual environment. You'll see a new folder appear with the Python installation named venv_name.

3. In the terminal, enter source venv_name/bin/activate. You'll notice that the command line now shows (venv_name)at the beginning of the line to indicate you are using the venv_name virtual environment.

4. Enter pip install stat-dist/. That should install the distributions Python package.

5. Try using the package in a program to see if everything works!
"""
