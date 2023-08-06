import openml
from openml.datasets import create_dataset

from road_safety import *

openml.config.apikey = '521c07a61128c83c43c9d62b2f607e5b'
df = get_road_safety_df()

params = {
    'name': 'road_safety',
    'description': 'Data reported to the police about the circumstances of personal injury road accidents in Great '
                   'Britain from 1979, and the maker and model information of vehicles involved in the respective '
                   'accident',
    'creator': 'Department for Transport UK',
    'contributor': None,
    'language': 'English',
    'licence': 'Open Government License',
    'collection_date': '2018-10-12',
    'attributes': 'auto',
    'data': df,
    'ignore_attribute': None,
    'default_target_attribute': 'Sex_of_Driver',
    'row_id_attribute': df.index.name,
    'citation': None,
    'version_label': '0.1',
    'original_data_url': ROAD_SAFETY_CONFIG.urlinfos[0].url,
    'paper_url': ROAD_SAFETY_CONFIG.source,
    'update_comment': None
}

print(df.info())

dset = create_dataset(**params)
open_ml_id = dset.publish()
print(open_ml_id.openml_url)
