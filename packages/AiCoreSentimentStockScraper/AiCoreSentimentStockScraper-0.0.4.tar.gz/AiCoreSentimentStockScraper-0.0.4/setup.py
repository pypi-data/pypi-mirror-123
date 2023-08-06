from os import path
from setuptools import setup
from setuptools import find_packages


setup(
    name='AiCoreSentimentStockScraper', ## This will be the name your package will be published with
    version='0.0.4', 
    description='scraping stock data',
    #url='https://github.com/IvanYingX/project_structure_pypi.git', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Tamim Ehsan', # Your name
    license='MIT',
    
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['beautifulsoup4', 'lxml','numpy','pandas','psycopg2-binary', 'requests', 'SQLAlchemy', 'tqdm','urllib3','vaderSentiment'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)