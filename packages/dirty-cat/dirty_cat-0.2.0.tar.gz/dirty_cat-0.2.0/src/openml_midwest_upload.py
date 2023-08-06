import openml
import pandas as pd
from openml.datasets import create_dataset

from midwest_survey import *

openml.config.apikey = '521c07a61128c83c43c9d62b2f607e5b'
df = get_midwest_survey_df()

new_cols = {'In your own words, what would you call the part of the country you live in now?': 'What_would_you_call_the_part_of_the_country_you_live_in_now',
            'How much, if at all, do you personally identify as a Midwesterner?': 'How_much_do_you_personally_identify_as_a_Midwesterner',
            'Do you consider Illinois state as part of the Midwest?': 'Do_you_consider_Illinois_state_as_part_of_the_Midwest',
            'Do you consider Indiana state as part of the Midwest?': 'Do_you_consider_Indiana_state_as_part_of_the_Midwest',
            'Do you consider Iowa state as part of the Midwest?': 'Do_you_consider_Iowa_state_as_part_of_the_Midwest',
            'Do you consider Kansas state as part of the Midwest?': 'Do_you_consider_Kansas_state_as_part_of_the_Midwest',
            'Do you consider Michigan state as part of the Midwest?': 'Do_you_consider_Michigan_state_as_part_of_the_Midwest',
            'Do you consider Minnesota state as part of the Midwest?': 'Do_you_consider_Minnesota_state_as_part_of_the_Midwest',
            'Do you consider Missouri state as part of the Midwest?': 'Do_you_consider_Missouri_state_as_part_of_the_Midwest',
            'Do you consider Nebraska state as part of the Midwest?': 'Do_you_consider_Nebraska_state_as_part_of_the_Midwest',
            'Do you consider North Dakota state as part of the Midwest?': 'Do_you_consider_North_Dakota_state_as_part_of_the_Midwest',
            'Do you consider Ohio state as part of the Midwest?': 'Do_you_consider_Ohio_state_as_part_of_the_Midwest',
            'Do you consider South Dakota state as part of the Midwest?': 'Do_you_consider_South_Dakota_state_as_part_of_the_Midwest',
            'Do you consider Wisconsin state as part of the Midwest?': 'Do_you_consider_Wisconsin_state_as_part_of_the_Midwest',
            'Do you consider Arkansas state as part of the Midwest?': 'Do_you_consider_Arkansas_state_as_part_of_the_Midwest',
            'Do you consider Colorado state as part of the Midwest?': 'Do_you_consider_Colorado_state_as_part_of_the_Midwest',
            'Do you consider Kentucky state as part of the Midwest?': 'Do_you_consider_Kentucky_state_as_part_of_the_Midwest',
            'Do you consider Oklahoma state as part of the Midwest?': 'Do_you_consider_Oklahoma_state_as_part_of_the_Midwest',
            'Do you consider Pennsylvania state as part of the Midwest?': 'Do_you_consider_Pennsylvania_state_as_part_of_the_Midwest',
            'Do you consider West Virginia state as part of the Midwest?': 'Do_you_consider_West_Virginia_state_as_part_of_the_Midwest',
            'Do you consider Montana state as part of the Midwest?': 'Do_you_consider_Montana_state_as_part_of_the_Midwest',
            'Do you consider Wyoming state as part of the Midwest?': 'Do_you_consider_Wyoming_state_as_part_of_the_Midwest',
            'In what ZIP code is your home located? (enter 5-digit ZIP code; for example, 00544 or 94305)': 'In_what_ZIP_code_is_your_home_located',
            "Household Income": "Household_Income",
            'Location (Census Region)': 'Census_Region'}

df.rename(columns=new_cols, inplace=True)

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

df = df.dropna(subset=['Census_Region'])  # Remove empty targets

# print(df[pd.isna(df['Census_Region']) == True])  # List empty targets (should be 0)

params = {
    'name': 'Midwest_survey',
    'description': 'Survey to know if people self-identify as Midwesterners.',
    'creator': 'FiveThirtyEight',
    'contributor': None,
    'language': 'English',
    'licence': 'Creative Commons Attribution 4.0 International License',
    'collection_date': '2014-04-30',
    'attributes': 'auto',
    'data': df,
    'ignore_attribute': None,
    'default_target_attribute': 'Census_Region',
    'row_id_attribute': df.index.name,
    'citation': None,
    'version_label': '0.1',
    'original_data_url': MIDWEST_SURVEY_CONFIG.urlinfos[0].url,
    'paper_url': MIDWEST_SURVEY_CONFIG.source,
    'update_comment': None
}

dset = create_dataset(**params)
open_ml_id = dset.publish()
print(open_ml_id.openml_url)
