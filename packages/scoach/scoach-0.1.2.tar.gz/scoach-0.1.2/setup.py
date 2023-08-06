# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scoach', 'scoach.cli', 'scoach.settings']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.0,<4.0.0',
 'Jinja2>=3.0.0,<4.0.0',
 'PyYAML>=5.4.0,<6.0.0',
 'dask_jobqueue>=0.7.0,<0.8.0',
 'loguru>=0.5.0,<0.6.0',
 'minio>=7.0.0,<8.0.0',
 'prefect>=0.15.0,<0.16.0',
 'psycopg2-binary>=2.9.0,<3.0.0',
 'tensorflow>=2.0.0,<3.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['scoach = scoach.cli:app']}

setup_kwargs = {
    'name': 'scoach',
    'version': '0.1.2',
    'description': 'Setup for training Tensorflow models on SLURM clusters.',
    'long_description': "# scoach\n\nA setup for training Tensorflow models on SLURM clusters\n\n## How does it work?\n\n- Inputs needed (see examples directory):\n  - A `.json` file with parameters for training\n  - A `.json` file with the model definition\n  - A `.py` file with the training code.\n  - There's a CLI app for interacting with scoach\n  - Run `scoach init` for setting up your configuration file, such as in `config_example.yaml`\n  - On the login machine at the SLURM cluster, run `scoach start`. This will start a daemon that will then launch jobs as requested.\n  - On any machine, you can do `scoach run submit` to submit jobs.\n  - This will upload the Python script to MinIO and submit the configurations to the database.\n  - The new runs are consumed by the daemon process, which then uses Jinja2 to render the training script and submit it to the cluster.\n  - The training script is then run on the cluster, using Dask workers, that will grow as needed.\n\n## To do\n\n- [ ] Add support for uploading/managing datasets\n- [ ] No Python script duplicates\n",
    'author': 'Gabriel Gazola Milan',
    'author_email': 'gabriel.gazola@poli.ufrj.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gabriel-milan/scoach',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
