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
# Replace 'Yes', 'No' and 'Do not know' by 1,2 and 3 respectively
df.replace({'Yes': 1, 'No': 2, 'Do not know':3}, inplace=True)

# Removing respondents outside the age range (Q13)
df = df[(df['Q13Age'] >= 7) & (df['Q13Age'] <= 17)]


# There appears to be trailing/leading whitespaces preventing some categories to be replaced in (Q26)
df['Q26Miss_Rsn'] = df['Q26Miss_Rsn'].str.strip()

# Replacing str by int (Q26)
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
    'To look after siblings':10,
    'Looking after a sick household member':11,
    'Looking after own children':12,
    'School vacation period':13,
    'Did not want to/feel like going to school':14,
    'Other, specify':15,
}, inplace=True)

# Removing missing values (Q52)
df = df.dropna(subset=['Q52ABEG_LSTW'])


# Exporting merged.csv
df.to_csv('merged.csv', index=False)
