# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geobr']

package_data = \
{'': ['*'], 'geobr': ['data/*']}

install_requires = \
['geopandas>=0.7.0,<0.8.0', 'shapely>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'geobr',
    'version': '0.1.10a1',
    'description': 'geobr: Download Official Spatial Data Sets of Brazil',
    'long_description': '# geobr Python Version\n\n## Behavior\n\n```python\npython\n>>> import geobr\n>>> geobr.read_biomes(year=2019)\n```\n\n## Contribute\n\nTo start the development environment run\n\n```sh\nmake\n. .venv/bin/activate\n```\n\nTest with\n\n`python -m pytest`\n\nYou can use a helper to translate a function from R.\nIf you want to add `read_biomes`, just run\n\n`python helpers/translate_from_R.py read_biomes`\n\nIt will scrape the original R function to get documentation and metadata.\nIt adds:\n- default year\n- function name\n- documentation one liner\n- larger documentation\n- very basic tests\n\n! Be aware that if the function that you are adding is more complicated than the template. So, double always double check !\n\nBefore pushing, run\n\n`make prepare-push`\n\n#### For Windows\n\nWe recommend using conda  and creating an environment that includes all libraries simultaneously.\n\nFirst create an environment and install Shapely and GDAL as such:\n\n`conda create --name geobr_env python=3.7`\n\nActivate the environmnet\n\n`conda activate geobr_env`\n\nThen add Shapely from conda-forge channel\n `conda install shapely gdal -c conda-forge`\n\nThen the other packages \n`conda install fiona pandas geopandas requests -c conda-forge`\n\n**Alternatively**, type on a terminal \n\n`conda create --name <env> --file conda_requirements.txt`\n\nFinally, if **not** using conda, try:\n\n`pip install -r pip_requirements.txt`\n\n## Translation Status\n\n| Function                 | Translated? | Easy? |\n|--------------------------|-------------|-------|\n| read_amazon              | Yes         | Super |\n| read_biomes              | Yes         | Super |\n| read_census_tract        | Yes         | No    |\n| read_conservation_units  | Yes         | Super |\n| read_country             | Yes         | Super |\n| read_disaster_risk_area  | Yes         | Super |\n| read_health_facilities   | Yes         | Super |\n| read_health_region       | Yes         | Super |\n| read_immediate_region    | Yes         | Yes   |\n| read_indigenous_land     | Yes         | Super |\n| read_intermediate_region | Yes         | Yes   |\n| read_meso_region         | Yes         | No    |\n| read_metro_area          | Yes         | Super |\n| read_micro_region        | Yes         | No    |\n| read_municipal_seat      | Yes         | Super |\n| read_municipality        | Yes         | No    |\n| read_region              | Yes         | Super |\n| read_semiarid            | Yes         | Super |\n| read_state               | Yes         | Super |\n| read_statistical_grid    | No          | No    |\n| read_urban_area          | Yes         | Super |\n| read_urban_concentrations| No          | Super |\n| read_weighting_area      | Yes         | No    |\n| list_geobr               | Yes         | Yes   |\n| lookup_muni              | Yes         | No    |\n| read_neighborhood        | Yes         | Yes   |\n\n\n\n',
    'author': 'João Carabetta',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ipeaGIT/geobr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
