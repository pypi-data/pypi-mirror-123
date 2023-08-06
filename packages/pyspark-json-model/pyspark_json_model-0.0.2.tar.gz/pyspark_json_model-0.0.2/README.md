[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Easily Parse your JSON & convert to relational data model format. This is currenlty build to support on Databricks/Pyspark

# Description
    
This package if for converting any json formatted data to relational data model in dataframe format for databricks

- `jsontools`: tools to parse json & converts to relational data model format

# Installation
 
## Normal installation

```bash
pip install pyspark_json_model
```

## Development installation

```bash
git clone https://github.com/rohitpawar95/pyspark_json_model.git
cd pyspark_json_model
pip install --editable .
```

## Usage

```
from pyspark_json_model import *

json2model_obj = jsontools.JSONParserPyspark('filepath_of_json', 
			<identifier_for_json_document:str>, 
		 	<is_looking_for_normalized_dataframe:bool>)

normalized_json_model = json2model_obj.process(sc, spark, ['drop_columns',...])

display(normalized_json_model[key])

Note: 
	is_looking_for_normalized_dataframe --> if True : The returned normalized_json_model 
	will hold extra key for root_node+'_normalized' which will have normalized json 
	format (This will be same as json_normalize function of pandas)

	is_looking_for_normalized_dataframe --> if False : The returned normalized_json_model 
	will just contain multiple keys which will hold independent tables of data model 
		
	normalized_json_model : This will be dictionary of data model key will be table name 
	and value will be dataframe corresponding to this key
	
	Pass sparkContext (sc) & sparkSession (spark) to process JSON along with 
	['drop_columns'] : The parameter to process() function is optional if need to remove 
	any columns while making this dataframe specify column list here

```
