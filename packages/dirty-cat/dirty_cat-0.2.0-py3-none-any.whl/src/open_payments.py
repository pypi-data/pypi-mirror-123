import os
from collections import namedtuple
from unittest import mock

import pandas as pd

from common.file_management import fetch, write_df, _uncompress_file

amount = ['Total_Amount_of_Payment_USDollars']
corp = ['Applicable_Manufacturer_or_Applicable_GPO_Making_' + 'Payment_Name']
dev_nm = ['Name_of_Associated_Covered_Device_or_Medical_Supply1']
dispute = ['Dispute_Status_for_Publication']
drug_nm = ['Name_of_Associated_Covered_Drug_or_Biological1']
pi_specialty = ['Physician_Specialty']
temp = ["Physician_Profile_ID", "Physician_First_Name",  "Physician_Middle_Name", "Physician_Last_Name"]

df_cols = pi_specialty + drug_nm + dev_nm + corp + dispute + temp

DatasetInfo = namedtuple('DatasetInfo', ['name', 'urlinfos', 'main_file', 'source'])
UrlInfo = namedtuple('UrlInfo', ['url', 'filenames', 'uncompress'])

OPEN_PAYMENTS_CONFIG = DatasetInfo(
    name='open_payments',
    urlinfos=
    (
        UrlInfo(
            url='https://download.cms.gov/openpayments/PGYR13_P063020.ZIP',
            filenames=None, uncompress=True
        ),
    ),
    main_file='open_payments.csv',
    source='https://openpaymentsdata.cms.gov'
)


def _get_file_paths(directory):
    #f = {file: os.path.join(directory, file) for file in os.listdir(directory) if
    #     '.txt' not in file and 'REMOVED' not in file and 'OWNRSHP' not in file}
    f = {
        "OP_DTL_GNRL_PGYR2013_P06302020.csv": "C:\\Users\\Phaide\\Dropbox\\Python\\dirty_cat\\src\\data\\open_payments\\output\\OP_DTL_GNRL_PGYR2013_P06302020.csv",
        "OP_DTL_RSRCH_PGYR2013_P06302020.csv": "C:\\Users\\Phaide\\Dropbox\\Python\\dirty_cat\\src\\data\\open_payments\\output\\OP_DTL_RSRCH_PGYR2013_P06302020.csv",
    }
    return f


def _process_df(files):
    #pd.set_option('display.max_rows', None)
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.width', None)
    #pd.set_option('display.max_colwidth', None)

    res_df = pd.DataFrame()

    for key in files:
        df = pd.read_csv(files[key])
        #df = df[df_cols]

        if 'RSRCH' in key:
            df['status'] = 'allowed'
        elif 'GNRL' in key:
            df['status'] = 'disallowed'

        #df = df.drop_duplicates(keep='first')
        res_df = pd.concat([res_df, df], ignore_index=True, sort=True)

    res_df = res_df.drop_duplicates(keep='first')
    return res_df


@mock.patch("common.file_management._check_dir")
def get_open_payment_df(mock_check_dir, save=True):
    mock_check_dir.return_value = (['C:\\Users\\Phaide\\Dropbox\\Python\\dirty_cat\\src\\data\\open_payments\\raw',
                                    'C:\\Users\\Phaide\\Dropbox\\Python\\dirty_cat\\src\\data\\open_payments\\output'],
                                   True)
    data_dir = fetch(OPEN_PAYMENTS_CONFIG)
    files = _get_file_paths(data_dir[0])
    _uncompress_file("C:\\Users\\Phaide\\Dropbox\\Python\\dirty_cat\\src\\data\\open_payments\\raw\\PGYR13_P063020.ZIP",
                     "C:\\Users\\Phaide\\Dropbox\\Python\\dirty_cat\\src\\data\\open_payments\\output", False)
    df = _process_df(files)
    df['Physician_Specialty'] = df['Physician_Specialty'].astype('category')
    df['Contextual_Information'] = df['Contextual_Information'].astype('string')
    df['Recipient_Postal_Code'] = df['Recipient_Postal_Code'].astype('string')
    df['NDC_of_Associated_Covered_Drug_or_Biological1'] = df['NDC_of_Associated_Covered_Drug_or_Biological1'].astype('string')
    df['NDC_of_Associated_Covered_Drug_or_Biological2'] = df['NDC_of_Associated_Covered_Drug_or_Biological2'].astype('string')
    df['NDC_of_Associated_Covered_Drug_or_Biological3'] = df['NDC_of_Associated_Covered_Drug_or_Biological3'].astype('string')
    df['NDC_of_Associated_Covered_Drug_or_Biological4'] = df['NDC_of_Associated_Covered_Drug_or_Biological4'].astype('string')
    df['NDC_of_Associated_Covered_Drug_or_Biological5'] = df['NDC_of_Associated_Covered_Drug_or_Biological5'].astype('string')
    df['Name_of_Associated_Covered_Device_or_Medical_Supply2'] = df['Name_of_Associated_Covered_Device_or_Medical_Supply2'].astype('string')
    df['Principal_Investigator_1_Postal_Code'] = df['Principal_Investigator_1_Postal_Code'].astype('string')
    df['Principal_Investigator_2_Zip_Code'] = df['Principal_Investigator_2_Zip_Code'].astype('string')
    df['Principal_Investigator_3_Zip_Code'] = df['Principal_Investigator_3_Zip_Code'].astype('string')
    df['Principal_Investigator_4_Zip_Code'] = df['Principal_Investigator_4_Zip_Code'].astype('string')
    df['Principal_Investigator_5_Zip_Code'] = df['Principal_Investigator_5_Zip_Code'].astype('string')
    df['Principal_Investigator_5_Zip_Code'] = df['Principal_Investigator_5_Zip_Code'].astype('string')
    df['Recipient_Zip_Code'] = df['Recipient_Zip_Code'].astype('string')
    # Vérifier les types des Series et les adapter au besoin.
    # ValueError: The dtype 'mixed' of the column 'NDC_of_Associated_Covered_Drug_or_Biological2' is not currently supported by liac-arff. Supported dtypes are categorical, string, integer, floating, and boolean.
    write_df(save, df, data_dir[1], OPEN_PAYMENTS_CONFIG.main_file)
    return df
