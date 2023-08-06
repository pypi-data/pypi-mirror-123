from collections import namedtuple

import pandas as pd

from common.file_management import write_df

DatasetInfo = namedtuple('DatasetInfo', ['name', 'urlinfos', 'main_file', 'source'])
UrlInfo = namedtuple('UrlInfo', ['url', 'filenames', 'uncompress','encoding'])

DRUG_DIRECTORY_CONFIG = DatasetInfo(
    name='drug_directory',
    urlinfos=(
        UrlInfo(
            url="https://www.accessdata.fda.gov/cder/ndctext.zip",
            filenames=(
                "product.txt",
                "package.txt",
            ),
            uncompress=True,
            encoding='latin-1'
        ),
    ),
    main_file="product.txt",
    source="https://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm"
)


def get_drug_directory_df(save=True):
    #data_dir = fetch(DRUG_DIRECTORY_CONFIG)
    #file = os.listdir(data_dir[0])[0]
    csv_path = "C:\\Users\\Phaide\\Dropbox\\Python\\github\\dirty_cat\\src\\data\\drug_directory\\raw\\ndctext\\product.csv"
    df = pd.read_csv(csv_path, sep=",", quotechar='"', escapechar="\\")
    out_path = "C:\\Users\\Phaide\\Dropbox\\Python\\github\\dirty_cat\\src\\data\\drug_directory\\output"
    write_df(save, df, out_path, DRUG_DIRECTORY_CONFIG.main_file)
    return df
