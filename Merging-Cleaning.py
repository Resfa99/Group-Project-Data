import pandas as pd

# Importing the data
df1 = pd.read_csv('dataset1.csv')
df2 = pd.read_csv('dataset2.csv')
df3 = pd.read_csv('dataset3.csv')

# Merging the datasets
merged = pd.merge(df1, df2, on='UQNO')
df = pd.merge(merged, df3, on='ID')

# Replacing the Q54TIME_DAY and Q72TIME_DAY columns by a single Q54TIME and Q72TIME column
df.drop(['Q54TIME', 'Q72TIME'], axis=1, inplace=True)

df.insert(loc=41, column='Q54TIME', value=df3.iloc[:, 1:8].sum(axis=1))
df.insert(loc=49, column='Q72TIME', value=df3.iloc[:, 8:15].sum(axis=1))
df.drop(df.columns[73:87], axis=1, inplace=True)

# Removing respondents outside the age range (Q13)
df = df[(df['Q13Age'] >= 7) & (df['Q13Age'] <= 17)]

# Replacing missing values in (Q16) and (Q15) (if mother is part of household, they're alive)
df.loc[(df['Q16Mothparthh'] == 'Yes') & (df['Q15Mothaliv'].isna()), 'Q15Mothaliv'] = 'Yes'
# If mother is dead, or respondent doesn't know, they're not part of household
df.loc[(df['Q15Mothaliv'].isin(['No', 'Do not know'])) & (df['Q16Mothparthh'].isna()), 'Q16Mothparthh'] = 'No'

# Same thing for (Q17) and (Q18)
df.loc[(df['Q18Fathparthh'] == 'Yes') & (df['Q17Fathaliv'].isna()), 'Q17Fathaliv'] = 'Yes'
df.loc[(df['Q17Fathaliv'].isin(['No', 'Do not know'])) & (df['Q18Fathparthh'].isna()), 'Q18Fathparthh'] = 'No'

# Rename some values and replacing missing values with 'Other'
df['Q23Eduinst'].replace({'Pre-school (including day care, crèche, pre-primary, ECD centre)': 'Pre-school',
                          'Higher educational institution (University/University of Technology)': 'Higher educational institution',
                          'Any other than the above, specify': 'Other'}, inplace=True)

df['Q23Eduinst'] = df['Q23Eduinst'].fillna('Other')

# Removing values above 12 and below 4 for first grade (Q24)
df = df[(df['Q24AGE_GR1'].isna()) | ((df['Q24AGE_GR1'] >= 4) & (df['Q24AGE_GR1'] <= 12))]


# There appears to be trailing/leading whitespaces in (Q26)
df['Q26Miss_Rsn'] = df['Q26Miss_Rsn'].str.strip()

# Replacing nan values by 'Not_Absent' in (Q26) to signify that they answered no for (Q25)
df['Q26Miss_Rsn'] = df['Q26Miss_Rsn'].fillna('Not_Absent')

# Fill missing values in (Q28) with 'Yes' where (Q22) is 'Yes'
df.loc[(df['Q22Attend'] == 'Yes') & (df['Q28Everattend'].isna()), 'Q28Everattend'] = 'Yes'

# Delete rows where (Q22) is 'Yes' and (Q28) is 'No'
df = df.loc[~((df['Q22Attend'] == 'Yes') & (df['Q28Everattend'] == 'No')), :]


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


# Noticing that some respondents said "Yes" to some questions and then 0 for the time associated (Q51)
df.loc[df['Q51TIME'] == 0, 'Q51EXTRAWORK_W'] = 'No'

# Removing missing values (Q52)
df = df.dropna(subset=['Q52ABEG_LSTW'])

# Removing (Q73) since it holds the exact same values as (Q22)
df.drop('Q73ATTEND', axis=1, inplace=True)

# Filter the rows where (Q71ACOOK) to (Q71GOTHR) are equal to 'No'
mask = (df['Q71ACOOK'] == 'No') & (df['Q71BCLEAN'] == 'No') & (df['Q71CLAUNDRY'] == 'No') & (df['Q71DCHILDMIND'] == 'No') & (
            df['Q71EMAINTENANCE'] == 'No') & (df['Q71FSHOP'] == 'No') & (df['Q71GOTHR'] == 'No')
filtered_df = df[mask]


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
df.drop(df.columns[[44, 45, -1]], axis=1, inplace=True)


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


# Replacing Child_Labour by No and Yes (for future purposes)
df['Child_Labour'] = df['Child_Labour'].replace({0: 'No', 1: 'Yes'})
# Exporting merged.csv
df.to_csv('merged.csv', index=False)

print(df.info())
print(df['Child_Labour'].unique())
