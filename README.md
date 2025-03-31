# kinetics_modelling

Retrieval and analysis of PacBio kinetics data from BAM files in the context of observed mutation data.

## Project Organization

```
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- Read it.
├── configs            <- INI files for run specific configurations (samples, context parameters, etc)
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── models             <- Placeholder for when the projects involves making predictions with the data
│
├── notebooks          <- ipynb files... but we're moving away from these
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── environment.yml   <- tracks the list of dependencies for the 
│                        project, triggerd by make create_environment Remember
│                        to conda env export > environment.yml
│
│
└── kinetics_modelling   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes kinetics_modelling a Python module
    │
    ├── config.py               <- General config information (paths, etc) and config loading func
    │
    ├── dataset.py              <- holds tools to generate data
    │
    ├── features.py             <- holds tools for feature generation
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- holds tools for generating predictions models          
    │   └── train.py            <- holds tools for training models
    │
    └── plots                   <- holds individual files for plotting, all stored in ../reports/figures         
    │   ├──  
    │   ├── predict.py                 
```

--------

