import openml
from openml.datasets import create_dataset

from drug_directory import *
import pandas as pd

openml.config.apikey = '521c07a61128c83c43c9d62b2f607e5b'
df = get_drug_directory_df()

columns_info = {
    "PRODUCTID": ["Product_ID", "string"],
    "PRODUCTNDC": ["Product_NDC", "string"],
    "PRODUCTTYPENAME": ["Product_type_name", "category"],
    "PROPRIETARYNAME": ["Proprietary_name", "category"],
    "PROPRIETARYNAMESUFFIX": ["Proprietary_name_suffix", "category"],
    "NONPROPRIETARYNAME": ["Non_proprietary_name", "category"],
    "DOSAGEFORMNAME": ["Dosage_form_name", "category"],
    "ROUTENAME": ["Route_name", "category"],
    "STARTMARKETINGDATE": ["Start_marketing_date", "string"],
    "ENDMARKETINGDATE": ["End_marketing_date", "string"],
    "MARKETINGCATEGORYNAME": ["Marketing_category_name", "category"],
    "APPLICATIONNUMBER": ["Application_number", "string"],
    "LABELERNAME": ["Labeler_name", "category"],
    "SUBSTANCENAME": ["Substance_name", "category"],
    "ACTIVE_NUMERATOR_STRENGTH": ["Active_numerator_strength", "string"],
    "ACTIVE_INGRED_UNIT": ["Active_ingred_unit", "category"],
    "PHARM_CLASSES": ["Pharm_classes", "category"],
    "DEASCHEDULE": ["DEA_schedule", "string"],
    "NDC_EXCLUDE_FLAG": ["NDC_exclude_flag", "category"],
    "LISTING_RECORD_CERTIFIED_THROUGH": ["Listing_record_certified_through", "string"],
}

new_cols = {key: value[0] for key, value in columns_info.items()}
cols_types = {value[0]: value[1] for value in columns_info.values()}

df.rename(columns=new_cols, inplace=True)
for col in df.columns:
    new_type = cols_types[col]
    df[col] = df[col].astype(new_type)

params = {
    'name': 'drug_directory',
    'description': 'Product listing data submitted to the U.S. FDA for all unfinished, unapproved drugs.',
    'creator': 'U.S. Food and Drug Administration',
    'contributor': None,
    'language': 'English',
    'licence': 'Public Domain (CC0)',
    'collection_date': '2016-09-09',
    'attributes': 'auto',
    'data': df,
    'ignore_attribute': None,
    'default_target_attribute': 'Active_numerator_strength',
    'row_id_attribute': df.index.name,
    'citation': None,
    'version_label': '0.1',
    'original_data_url': DRUG_DIRECTORY_CONFIG.urlinfos[0].url,
    'paper_url': DRUG_DIRECTORY_CONFIG.source,
    'update_comment': None
}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print(df.info())

dset = create_dataset(**params)
open_ml_id = dset.publish()
print(open_ml_id.openml_url)
