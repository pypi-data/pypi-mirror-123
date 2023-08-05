from os import path
from setuptools import setup
from setuptools import find_packages


setup(
    name='AiCoreSentimentStockScraper2021EtaCohort', ## This will be the name your package will be published with
    version='0.0.2', 
    description='scraping stock data',
    #url='https://github.com/IvanYingX/project_structure_pypi.git', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Tamim Ehsan', # Your name
    license='MIT',
    
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['beautifulsoup4','bs4','certifi','charset-normalizer','colorama','greenlet','idna','lxml','numpy','pandas','pyscopg2-binary','python-dateutil','pytz','requests','six','soupsieve','SQLAlchemy','tqdm','urllib3','vaderSentiment'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)