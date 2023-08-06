from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='pyspark_json_model',
    version='0.0.3',
    description='JSON to Relational data model through Pyspark using Databricks',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Rohit Pawar',
    author_email='rohitpawar95@outlook.com',
    keywords=['Pyspark', 'Spark', 'JSON', 'Data Model', 'Python', 'JSON Flatten', 'Databricks'],
    url='https://github.com/rohitpawar95/pyspark_json_model',
    download_url='https://pypi.org/project/pyspark_json_model/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
