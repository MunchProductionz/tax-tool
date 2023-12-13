# Running the code locally

## Conda

Download Anaconda using the Anaconda installer:

- (Download Anaconda)[`https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html`]

Open the Anaconda terminal.
Create conda environment and install Python:

- `conda create -n <environment-name>`

Activate the environment using:

- `conda activate <environment-name>`

Install python to get access to pip:

- `conda install python`

Make all necessary imports using:

- `pip install -r requirements.txt`

*Created the `requirements.txt` file using:

- `conda list -e > requirements.txt`*