import pandas as pd

# Importing the data
df = pd.read_csv('dataset_unlabelled.csv')


# Replacing missing values in (Q16) and (Q15) (if mother is part of household, they're alive)
df.loc[(df['Q16Mothparthh'] == 'Yes') & (df['Q15Mothaliv'].isna()), 'Q15Mothaliv'] = 'Yes'
# If mother is dead, or respondent doesn't know, they're not part of household
df.loc[(df['Q15Mothaliv'].isin(['No', 'Do not know'])) & (df['Q16Mothparthh'].isna()), 'Q16Mothparthh'] = 'No'

# Same thing for (Q17) and (Q18)
df.loc[(df['Q18Fathparthh'] == 'Yes') & (df['Q17Fathaliv'].isna()), 'Q17Fathaliv'] = 'Yes'
df.loc[(df['Q17Fathaliv'].isin(['No', 'Do not know'])) & (df['Q18Fathparthh'].isna()), 'Q18Fathparthh'] = 'No'

# Replacing str by int (Q23)
df['Q23Eduinst'].replace({'Pre-school (including day care, crèche, pre-primary, ECD centre)': 1,
                          'Primary or secondary school': 2,
                          'Home based education/home schooling': 3,
                          'Higher educational institution (University/University of Technology)': 4,
                          'Literacy classes': 5,
                          'Further Education and Training College (FET)': 6,
                          'Other College': 7,
                          'Adult Basic Education and Training Learning centre (ABET centre)': 8,
                          'Any other than the above, specify': 9}, inplace=True)
df['Q23Eduinst'] = df['Q23Eduinst'].fillna(-1)



# There appears to be trailing/leading whitespaces in (Q26)
df['Q26Miss_Rsn'] = df['Q26Miss_Rsn'].str.strip()

# Fill missing values in (Q28) with 'Yes' where (Q22) is 'Yes'
df.loc[(df['Q22Attend'] == 'Yes') & (df['Q28Everattend'].isna()), 'Q28Everattend'] = 'Yes'


# Removing (Q29) to (Q212) columns since they don't give particularly useful information
df.drop(df.columns[17:21], axis=1, inplace=True)

# Replacing missing values by 0 for hours spent working (Q51)
df[['Q51ATIME',
    'Q51BTIME',
    'Q51CTIME',
    'Q51DTIME',
    'Q51ETIME',
    'Q51FTIME']] = df[['Q51ATIME',
                       'Q51BTIME',
                       'Q51CTIME',
                       'Q51DTIME',
                       'Q51ETIME',
                       'Q51FTIME']].fillna(0)


# Aggregating (Q51) under 2 new columns 'Q51EXTRAWORK_W' and 'Q51TIME'
df['Q51EXTRAWORK_W'] = df[['Q51AFARMWRK_W',
                           'Q51BFETCHWATER_W',
                           'Q51CFETCHWOOD_W',
                           'Q51DPRODHHGDS_W',
                           'Q51ECONSTRUC_W',
                           'Q51FCATCHFOOD_W']].apply(lambda row: 'Yes' if 'Yes' in row.values else 'No', axis=1)

df.insert(17, 'Q51EXTRAWORK_W', df.pop('Q51EXTRAWORK_W'))
df.insert(loc=18, column='Q51TIME', value=df.iloc[:, [19, 21, 23, 25, 27, 29]].sum(axis=1))
df.drop(df.columns[19:31], axis=1, inplace=True)


# Replacing missing values by 0 for hours spent working (Q54)
df['Q54TIME'] = df['Q54TIME'].fillna(0)

# Removing (Q73) since it holds the exact same values as (Q22)
df.drop('Q73ATTEND', axis=1, inplace=True)

# Filter the rows where (Q71ACOOK) to (Q71GOTHR) are equal to 'No'
mask = (df['Q71ACOOK'] == 'No') & (df['Q71BCLEAN'] == 'No') & (df['Q71CLAUNDRY'] == 'No') & (df['Q71DCHILDMIND'] == 'No') & (
            df['Q71EMAINTENANCE'] == 'No') & (df['Q71FSHOP'] == 'No') & (df['Q71GOTHR'] == 'No')
filtered_df = df[mask]

# Replacing missing values by 0 for hours spent working (Q72)
df['Q72TIME'] = df['Q72TIME'].fillna(0)

# Fill missing values in (Q741), (Q742) and (Q743) with 'No' for the filtered rows
filtered_df['Q741AFTERSCH'].fillna('No')
filtered_df['Q742BEFORESCH'].fillna('No')
filtered_df['Q743WEEKEND'].fillna('No')

# Update the original DataFrame with the filled values
df.update(filtered_df)

# Replacing missing values by 'No' for all (Q75) questions, if they don't attend school, they don't do any school chores
df[['Q75ACLEAN',
    'Q75BMAINTENANCE',
    'Q75CGARDEN',
    'Q75DMARK',
    'Q75EHOUSE',
    'Q75FOTHR']] = df[['Q75ACLEAN',
                       'Q75BMAINTENANCE',
                       'Q75CGARDEN',
                       'Q75DMARK',
                       'Q75EHOUSE',
                       'Q75FOTHR']].fillna('No')

# Aggregating (Q75) questions under 'Q75SCHOOL_CHORES'
df['Q75SCHOOL_CHORES'] = df[['Q75ACLEAN',
                               'Q75BMAINTENANCE',
                               'Q75CGARDEN',
                               'Q75DMARK',
                               'Q75EHOUSE',
                               'Q75FOTHR']].apply(lambda row: 'Yes' if 'Yes' in row.values else 'No', axis=1)

df.insert(39, 'Q75SCHOOL_CHORES', df.pop('Q75SCHOOL_CHORES'))
df.drop(df.columns[40:46], axis=1, inplace=True)

# Replacing missing values by 0 for hours spent working (Q76)
df['Q76TIME'] = df['Q76TIME'].fillna(0)

# Aggregating (Q77) into 'Q77Diff'
df['Q77DIFF'] = df[['Q77ADIF_CTCHUP',
                               'Q77BNOTIME',
                               'Q77CCONCENTRATE',
                               'Q77DPUNCTUAL',
                               'Q77ELEISURE',]].apply(lambda row: 'Yes' if 'Yes' in row.values else 'No', axis=1)

df.insert(41, 'Q77DIFF', df.pop('Q77DIFF'))
df.drop(df.columns[42:48], axis=1, inplace=True)

# The stratum already gives all the geographical information about the respondent, we can drop the other columns
df.drop(df.columns[[43, 44, -1]], axis=1, inplace=True)


# Aggregating (Q71) questions under 'Q71HHTASKS'
df['Q71HHTASKS'] = df[['Q71ACOOK',
                       'Q71BCLEAN',
                       'Q71CLAUNDRY',
                       'Q71DCHILDMIND',
                       'Q71EMAINTENANCE',
                       'Q71FSHOP',
                       'Q71GOTHR']].apply(lambda row: 'Yes' if 'Yes' in row.values else 'No', axis=1)

df.insert(28, 'Q71HHTASKS', df.pop('Q71HHTASKS'))
df.drop(df.columns[29:36], axis=1, inplace=True)


# Nominal to numerical values if not done already
# Replace 'Yes', 'No' and 'Do not know' by 1,2 and 3 respectively
df.replace({'Yes': 1, 'No': 2, 'Do not know': 3}, inplace=True)
# (Q12)
df['Q12Gender'].replace({'Male': 1,
                         'Female': 2}, inplace=True)
# (Q14)
df['Q14Population'].replace({'African/Black': 1,
                             'Coloured': 2,
                             'Indian/Asian': 3,
                             'White': 4,
                             'Other, specify': 5}, inplace=True)
# (Q26)
df['Q26Miss_Rsn'].replace({
    'Illness': 1,
    'Injury': 2,
    'School too far': 3,
    'Teacher was absent': 4,
    'No transport': 5,
    'Bad weather conditions': 6,
    'Working in household business': 7,
    'Working in non-household business': 8,
    'To help at home with household tasks': 9,
    'To look after siblings': 10,
    'Looking after a sick household member': 11,
    'Looking after own children': 12,
    'School vacation period': 13,
    'Did not want to/feel like going to school': 14,
    'Other, specify': 15,
}, inplace=True)

df['Q26Miss_Rsn'] = df['Q26Miss_Rsn'].fillna(-1)

# (Q27)
df['Q27Daysabsent'].replace({'0 days': 1,
                             '1 to 4 days': 2,
                             '5 to 9 days': 3,
                             '10 to 19 days': 4,
                             '20 or more days': 5,
                             'Unspecified': -1}, inplace=True)


# Exporting merged.csv
df.to_csv('unlabelled.csv', index=False)


print(df.info())

