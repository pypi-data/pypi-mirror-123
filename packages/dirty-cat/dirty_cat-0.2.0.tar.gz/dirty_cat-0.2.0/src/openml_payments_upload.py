import openml
import pandas as pd
from openml.datasets import create_dataset

from open_payments import *

openml.config.apikey = '58012f5a6cbba5dcd3ddefbf852c1e99'
# df = get_open_payment_df()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# df = df.convert_dtypes(infer_objects=True)


params = {
    'name': 'open_payments',
    'description': ('Payments given by healthcare manufacturing companies to medical doctors or hospitals.\n'
                    'About this dataset: '
                    'A simple way to predict from the dataset would be to limit the analysis to columns ['
                    '"Total_Amount_of_Payment_USDollars", '
                    '"Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name", '
                    '"Name_of_Associated_Covered_Device_or_Medical_Supply1", '
                    '"Dispute_Status_for_Publication", '
                    '"Name_of_Associated_Covered_Drug_or_Biological1", "Physician_Specialty", '
                    '"Physician_Profile_ID", "Physician_First_Name", "Physician_Middle_Name", "Physician_Last_Name"] '
                    'and drop the duplicated lines. '
                    'In the full dataset a given physician is represented several times.\n'
                    'Additional resources: Patricio Cerda, Gael Varoquaux. '
                    'Encoding high-cardinality string categorical variables. 2019. '
                    'https://hal.inria.fr/hal-02171256v4.'),
    'creator': 'Centers for Medicare & Medicaid Services',
    'contributor': None,
    'language': 'English',
    'licence': 'Public Domain (CC0)',
    'collection_date': '2018-01-01',
    'attributes': 'auto',
#    'data': df,
    'ignore_attribute': None,
    'default_target_attribute': 'status',
#    'row_id_attribute': df.index.name,
    'citation': None,
    'version_label': '0.1',
    'original_data_url': OPEN_PAYMENTS_CONFIG.urlinfos[0].url,
    'paper_url': OPEN_PAYMENTS_CONFIG.source,
    'update_comment': None
}

# print(df.dtypes)

print(params['description'])

# dset = create_dataset(**params)
#open_ml_id = dset.publish()
#print(dset.openml_url)
