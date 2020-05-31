import pandas as pd 
import altair as alt
import datetime

df = pd.read_excel("https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2020/05/COVID-19-total-announced-deaths-30-May-2020.xlsx", sheet_name="Tab4 Deaths by trust", skiprows=15, usecols="B:EA")

cols = list(df.columns)
cols = [c for c in cols if "Unnamed:" not in str(c)]
df = df[cols]

df = df.loc[:, "NHS England Region":"Total"]
df = df.iloc[2:, :]

dt_cols = [c for c in cols if type(c) == datetime.datetime]
other_cols = [c for c in cols if type(c) != datetime.datetime]

df = df.melt(id_vars = other_cols, value_vars=dt_cols)


df = df.sort_values(["Name", "variable"])
df["rs"] = df.groupby('Name')['value'].rolling(7).sum().reset_index(0,drop=True)


f1 = df["Name"].str.lower().str.contains("oxford university")
f2 = df["Name"].str.lower().str.contains("west hertfordshire")
f3 = df["Name"].str.lower().str.contains("cambridge university")

df.loc[f1|f2|f3, "highlight"] = "yes"
df.loc[~(f1|f2|f3), "highlight"] = "no"

df2 = df[f1|f2|f3]

alt.data_transformers.enable('json')
c1 = alt.Chart(df).mark_line().encode(
    x='variable',
    y='rs',
    color=alt.Color('Name',  scale=None),
    tooltip=['Name', "variable", "rs"]
)

c2 = alt.Chart(df2).mark_line().encode(
    x='variable',
    y='rs',
    color='Name',
    tooltip=['Name', "variable", "rs"]
)

c3 = (c1 + c2).properties(height=500, width=800)

with alt.data_transformers.enable('default'):
    c3.save('chart.png')

