from setuptools import setup, find_packages

with open("README.md", "r") as cd:
  long_description = cd.read()




setup(name = 'smart_dist',

      version = '1.0.0',
      
      license='MIT',
      
      description = 'Binomial and Gaussian distributions along with a Crypto Analytic Tool',
      
      long_description=long_description,
      
      long_description_content_type="text/markdown",
      
      packages = ['smart_dist'],
      
      author = 'Alao David I.',
      
      author_email = 'alaodavid41@gmail.com',
      
      url = 'https://github.com/invest41/smart-dist',
      
      
      install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'numpy',
        'plotly',
        'jupyter',
        'scikit-learn',
        'Joblib',
        'yfinance'
        ],
      
      zip_safe = False)
