
<p align="center">
  <img src="docs/docs/img/mappable.png" width="300" title="mappable logo"> 
  <p align="center">
  Interactive Data annotation, visualisation and recommendation.
  </p>
</p>

### Installation

mappable requires Python 3.6.1 or later.
The preferred way to install mappable is via `pip`. You can install it with:

 ```pip install mappable```

<details>
<summary>Setting up a virtual environment </summary>

[Conda](https://conda.io/) can be used set up a virtual environment with the
version of Python required for mappable.  If you already have a Python 3
environment you want to use, you can skip to the 'installing via pip' section.

1.  [Download and install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

2.  Create a Conda environment with Python 3.7 (3.6 or 3.8 would work as well):

    ```
    conda create -n mappable python=3.7
    ```

3.  Activate the Conda environment. You will need to activate the Conda environment in each terminal in which you want to use mappable:

    ```
    conda activate mappable
    ```
</details>

### Python Development

The Python service and Python cli are formatted using `black` and `flake8`. Currently this is run in a local environment
using the app's `requirements.txt`. To run the linters:

```
black api/
flake8 api/
```

### Development Prerequisites

Make sure that you have the latest version of [Docker 🐳](https://www.docker.com/get-started)
installed on your local machine.

To start a version of the application locally for development purposes, run
this command:

```
~ docker-compose up --build
```

This process launches 2 services, the `ui` and `api`. You'll see output
from each.

It might take a minute or two for the application to start, particularly
if it's the first time you've executed this command. Be patience and wait
for a clear message indicating that all of the required services have
started up.

As you make changes the running application will be automatically updated.
Simply refresh your browser to see them.

Sometimes one portion of your application will crash due to errors in the code.
When this occurs resolve the related issue and re-run `docker-compose up --build`
to start things back up.

### Deployment

Mappable is designed as a python package, with the UI packaged *inside* it. The package is built and pushed to Pypi when a git tag is pushed. This all happens in the `.github/workflows/publish.yml` in this repository.

The only difference to a standard package being built is that we first build the UI and copy it inside the `api/mappable/static` directory, which is where the mappable server looks to find the static UI files. Currently, this is done via the `build_ui.sh` script, which builds the UI inside a docker container and copies the result out, to make it easily replicable.