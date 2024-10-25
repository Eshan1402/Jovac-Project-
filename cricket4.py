import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from matplotlib import pyplot as plt

# Customizing the Title of the Presentation
st.title("Jovac Presentation")

# Load CSVs using st.cache_data
@st.cache_data
def load_data():
    ipl = pd.read_csv('ipl.csv')
    top10 = pd.read_csv('top10_score.csv')
    return ipl, top10

ipl, top10 = load_data()

# Display IPL Data
st.subheader("Top 10 Batsmen Data")
st.dataframe(ipl.head())

# Batsman Selection for Single Batsman Analysis
batsman = st.selectbox("Select a Batsman", ipl['batsman'].unique())
single = ipl[ipl['batsman'] == batsman]

# Plotting Performance for the selected batsman
try:
    performance = single.groupby('season')['batsman_runs'].sum().to_frame().reset_index()

    # Plot using Plotly with customized color
    st.subheader(f"{batsman}'s Year-by-Year Performance")
    trace = go.Scatter(x=performance['season'], y=performance['batsman_runs'],
                       mode='lines+markers', marker={'color': '#ff6347'}, name=batsman)  # Change color to '#ff6347'
    data = [trace]
    layout = go.Layout(title=f'{batsman} Year by Year Performance',
                       xaxis={'title': 'Season'},
                       yaxis={'title': 'Total Runs'})
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"Error: {e}")

# Plot for Top 10 Batsmen Total Runs with custom color
st.subheader("Top 10 IPL Batsmen")
trace = go.Bar(x=top10['batsman'], y=top10['batsman_runs'], marker_color='#4682b4')  # Change bar color to '#4682b4'
data = [trace]
layout = go.Layout(title='Top 10 IPL Batsmen', xaxis={'title': 'Batsman'}, yaxis={'title': 'Total Runs'})
fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)

# Innings Analysis
st.subheader("1st Innings vs 2nd Innings Comparison for Top 10 Batsmen")
top10_df = ipl[ipl['batsman'].isin(top10['batsman'])]
iw = top10_df.groupby(['batsman', 'inning'])['batsman_runs'].sum().reset_index()

mask = iw['inning'] == 1
mask2 = iw['inning'] == 2
one = iw[mask]
two = iw[mask2]
one.rename(columns={'batsman_runs': '1st Innings'}, inplace=True)
two.rename(columns={'batsman_runs': '2nd Innings'}, inplace=True)

final = one.merge(two, on='batsman')[['batsman', '1st Innings', '2nd Innings']]
st.dataframe(final)

# Plot 1st and 2nd Innings Run Distributions
st.subheader("Run Distribution: 2nd Innings")
fig, ax = plt.subplots()
final['2nd Innings'].plot(kind='hist', bins=20, title='2nd Innings Runs Distribution', ax=ax, color='#FF4500')  # Change histogram color
plt.gca().spines[['top', 'right']].set_visible(False)
plt.xlabel('Runs')
plt.ylabel('Frequency')
st.pyplot(fig)

st.subheader("Run Distribution: 1st Innings")
fig, ax = plt.subplots()
final['1st Innings'].plot(kind='hist', bins=20, title='1st Innings Runs Distribution', ax=ax, color='#4682B4')  # Change histogram color
plt.gca().spines[['top', 'right']].set_visible(False)
plt.xlabel('Runs')
plt.ylabel('Frequency')
st.pyplot(fig)