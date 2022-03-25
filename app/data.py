import pandas as pd
from IPython.display import display


# ----------------------------------------
# Data Preprocessing (importing and cleaning data)

df = pd.read_csv('./data/Data_Incidents_Raised.csv')

df.drop(['Incidenct Code','Customer Company','Incident Description','Support Group','Tower Group','Domain Group','Urgency','Resolution Description','Assigned Organization','Inc. Category','Last Modified Date','Inc. Element','Aging (Days)','Localización Cliente','Departamento Cliente'], axis=1, inplace=True)

df.drop(df.index[df['Customer Company Group'] == 'IAG CARGO'], inplace=True)
df.drop(df.index[df['Customer Company Group'] == 'IBERIA EXPRESS'], inplace=True)
df.drop(df.index[df['Customer Company Group'] == 'OTHERS'], inplace=True)
df.drop('Customer Company Group', axis=1, inplace=True)

df['Create Date-Time'] = pd.to_datetime(df['Create Date-Time'], dayfirst = True)
df['Resolution Date-Time'] = pd.to_datetime(df['Resolution Date-Time'], dayfirst = True)
df['time_to_resolve'] = df['Resolution Date-Time'] - df['Create Date-Time']

df['SLA'] = df.apply(lambda _: '', axis=1)
for i in df.index: 
    if df.Priority[i] == "Baja":
        df.at[i, 'SLA'] =  pd.Timedelta("15 days 00:00:00")
    elif df.Priority[i] == "Media":
        df.at[i, 'SLA'] =  pd.Timedelta("5 days 00:00:00")
    elif df.Priority[i] == "Alta":
        df.at[i, 'SLA'] =  pd.Timedelta("0 days 08:00:00")
    elif df.Priority[i] == "Crítica":
        df.at[i, 'SLA'] =  pd.Timedelta("0 days 04:00:00")

df['meets SLA?'] = df.apply(lambda _: '', axis=1)
for i in df.index:    
    if df.time_to_resolve[i] < df.SLA[i]:
        df.at[i, 'meets SLA?'] = "yes"
    elif df['Resolution Date-Time'].isnull()[i]:
        df.at[i, 'meets SLA?'] = "unresolved"
    else:
        df.at[i, 'meets SLA?'] = "no"

df['Priority'] = df['Priority'].replace(['Baja'],'Low')
df['Priority'] = df['Priority'].replace(['Media'],'Medium')
df['Priority'] = df['Priority'].replace(['Alta'],'High')
df['Priority'] = df['Priority'].replace(['Crítica'],'Critical')

df['Inc. Type'] = df['Inc. Type'].replace(['SECURITY ISSUE.INFORM. SECURITY POLICIES AND BEST PRACTICES'],'SECURITY ISSUE.INFORM.POLICIES')
df['Inc. Type'] = df['Inc. Type'].replace(['SECURITY ISSUE.PHYSICAL AND ENVIRONMENTAL SECURITY'],'SECURITY ISSUE.PHYSICAL SEC')



# display(df.head(10))
# display(df.tail(10))

dft = df.copy()

dft['Create Date-Time'] = dft['Create Date-Time'].dt.strftime('%Y-%m')

df1 = dft.groupby(['Create Date-Time','Priority'], sort = False).size().reset_index().rename(columns={0:'Incidents'})

df2 = dft.groupby(['Create Date-Time','Inc. Type'], sort = False).size().reset_index().rename(columns={0:'Incidents'})
df2t = dft.groupby(['Create Date-Time','Inc. Type'], sort = False)['time_to_resolve'].mean().reset_index()
for i in df2t.index:
    df2t['time_to_resolve'][i] = pd.Timedelta(df2t['time_to_resolve'][i]).round(freq = 's')
df2["Avg. Resolution Time"] = df2t['time_to_resolve'].astype(str)
df2 = df2.sort_values(by='Incidents', ascending=False)
# df2["Avg. Resolution Time"]

df3 = dft.groupby(['Priority','Create Date-Time','meets SLA?'], sort = True).size().reset_index().rename(columns={0:'Incidents'})

df4 = pd.get_dummies(dft, columns = ['meets SLA?'], drop_first = False)

df5 = dft

df5["Incidents"] = 1

df6 = df5

df7 = dft.groupby(['Create Date-Time'], sort = False).size().reset_index().rename(columns={0:'Incidents'})
df7.rename(columns={'Create Date-Time': 'Month'}, inplace = True)
df7['Month'] = df7['Month'].replace(['2021-01'],'January')
df7['Month'] = df7['Month'].replace(['2021-02'],'February')
df7['Month'] = df7['Month'].replace(['2021-03'],'March')
df7['Month'] = df7['Month'].replace(['2021-04'],'April')



# sla_yes = df7[(df7['Create Date-Time'] == '2021-01') & (df7['Priority'] == 'Low')]['meets SLA?_yes'].sum()
# sla_no = df7[(df7['Create Date-Time'] == '2021-01') & (df7['Priority'] == 'Low')]['meets SLA?_no'].sum()
# sla_unresolved = df7[(df7['Create Date-Time'] == '2021-01') & (df7['Priority'] == 'Low')]['meets SLA?_unresolved'].sum()

# display(sla_yes)
# display(sla_no)
# display(sla_unresolved)