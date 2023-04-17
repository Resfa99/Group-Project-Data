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
df['Q13Age'] = df['Q13Age'].clip(7, 17)
print(df['Q13Age'].min())


print(df)
df.to_csv('merged.csv', index=False)
