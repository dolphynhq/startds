# Start Data Science

_An opinionated, organized way to start and manage data science experiments._

Start Data Science is a template to help you set up experiments. It brings structure to exploratory data analysis (EDA), through to feature extraction, modeling, and resultant outputs whether they're figures, reports, APIs, or apps. 

&nbsp;

The main components are:

- A pre-defined framework creating organization for your experiment
- A pre-compiled `requirements.txt` featuring over 150 commonly used data science libraries
- Extensible scripts with boilerplate for Streamlit, Flask, FastAPI and Cortex.

- (Work in progress) A library of common helpers like writing and reading to S3, methods to clean, transform and extract features from data

- (Work in progress) Adding more open source solutions for apis and apps (eg BentoML)

&nbsp;

The idea of this repo is to provide a comprehensive structure. The user is to delete portions, and manipulate the dag accordingly per their experiment needs. 

&nbsp;

## Getting Started

1. Install the library
```sh
pip install startds
```

2. Create your first experiment
```sh
startds create <exp_name>
```

## Usage  
### Available Commands

- _create_
```sh
startds create <exp_name>
```

Creates a new experiment directory structure. where `exp_name` is the name of the new experiment you want to create. This will create a new folder named `exp_name` in the current folder.  
&nbsp;

- _env_
```sh
startds env [optional] -f <path_to_requirements.txt>
```

Initializes a virtual environment for the experiment with over 150 of the most commonly used data science libraries. Note, it installs `airflow` which is required in order to execute the dag.

To start the new virtual environment created, run
```sh
source .venv/bin/activate
```

&nbsp;

### Running the experiment

```python
python run.py
```
Runs `dag.py` which is configured using `airflow` by default. Note: you will require airflow, or you can configure using your preferred orchestrator. The dag can be easily modified to add or remove steps, and/or execute individual components.

&nbsp;

### Running tests

Tests are to be written in the _tests folder inside src folder. ```pytest``` package can be used to run these tests.
Make sure that ```pytest``` is installed and run
```sh
pytest
```
from the root directory or the ```_tests``` directory to run tests


## The resulting directory structure

The directory structure of your new project looks like this: 

```
├── README.md          <- The top-level README for developers using this project.
│
├── Dockerfile         <- Dockerfile to create docker images for K8s or other cloud services
|
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
|
├── setup.py           <- makes project pip installable (pip install -e .) to enable imports of sibling modules in src
|
├── run.py             <- Run file that calls an orchestrator or individual .py files in your project
|
├── exp_name           <- namesake folder inside the exp_name root folder that you created
|   |
|   ├── metadata           <- Metadata that needs to persisted and shared for data sources and models
|   │   └── data.md
|   │   └── models.md
|   |
|   ├── models             <- Trained and serialized models, model predictions, or model summaries
|   │
|   ├── outputs            <- Generated analysis as HTML, PDF, LaTeX, etc.
|   │   └── figures        <- Generated graphics and figures to be used in reporting
|   |
|   ├── src                <- Source code for use in this project.
|   │   ├── __init__.py    <- Makes src a Python module
|   |   |
|   |   ├── _apis          <- Scripts to create APIs for serving models using Flask/FastAPI/others
|   |   |   └── fastapi
|   |   |   |   └── main.py
|   |   |   |   └── Dockerfile
|   |   |   |   └── build.sh
|   |   |   |
|   |   |   └── flask
|   |   |   |   └── main.py
|   |   |   |   └── Dockerfile
|   |   |   |   └── build.sh
|   |   |   |
|   |   |   └── cortex
|   |   |       └── main.py
|   |   |       └── cortex.yaml
|   |   |       └── requirements.txt
|   |   |
|   │   ├── _apps          <- Scripts to create internal ML apps using streamlit, dash etc
|   |   |   └── streamlit
|   |   |       └── main.py
|   |   |       └── Dockerfile
|   |   |       └── build.sh
|   |   |
|   |   ├── _orchestrate       <- Scripts to run different steps of the project using an orchestrator such as airflow
|   │   |   └── airflow
|   |   |       └── dags
|   |   |           └── dag.py
|   |   |
|   │   ├── _tests         <- Scripts to add tests for your experiment
|   │   │   └── test_clean.py
|   |   |
|   │   ├── clean          <- Scripts to connect and clean data
|   │   │   └── clean_data.py
|   |   |   └── connect_data.py
|   |   |
|   │   ├── explore        <- Scripts to create exploratory and results oriented visualizations
|   │   |   └── visualize.py
|   │   |   └── explore.py
|   │   │
|   │   ├── transform      <- Scripts to turn raw data into features for modeling
|   │   │   └── transform_data.py
|   |   |   └── setup_experiment.py
|   │   │
|   │   ├── train          <- Scripts to train models and then use trained models to make predictions
|   │   │   ├── predict_model.py
|   │   │   └── train_model.py
|   |   |   └── model.py
|   │   │
```

&nbsp;


## Note about importing sibling modules

To enable importing sibling modules when writing code in src, it is best to install the root experiment as
a python package 
```sh
pip install -e .
```
You could also modify the ```sys.path``` in each file that wants to import sibling module
Another solution is to run files form the root folder using ```python3 -m absolute_import_path_to_module```

Some reference for this issue
[Sibling package imports](https://stackoverflow.com/questions/6323860/sibling-package-imports/23542795#23542795)

If you have ideas about how to manage this structure better, please let us know. 
&nbsp;


## Contributing to start-data-science

Feel free to open an issue against this repository or [contact us](mailto:support@dolphyn.io) and we'll help point you in the right direction.


## License

Released under the [MIT license](LICENSE).

## Acknowledgements

A huge thanks to the following projects:

### Structure / Inspiration:

[Django](https://github.com/django/django)  
[Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science/)

### Integrations:

[Streamlit](https://github.com/streamlit/streamlit)  
[Cortex](https://github.com/cortexlabs/cortex)  
[FastAPI](https://github.com/tiangolo/fastapi)  
[Flask](https://github.com/pallets/flask)  
[Airflow](https://github.com/apache/airflow)


