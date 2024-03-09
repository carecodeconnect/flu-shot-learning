import streamlit as st
import pandas as pd
import plotly.express as px

# Load your datasets
submission_format = pd.read_csv('data/submission_format.csv')
training_set_features = pd.read_csv('data/training_set_features.csv')
training_set_labels = pd.read_csv('data/training_set_labels.csv')
test_set_features = pd.read_csv('data/test_set_features.csv')

# Create a boolean DataFrame of missing values for all columns except 'respondent_id'
missing_values = training_set_features.drop(columns=['respondent_id']).isna()

# Calculate the sum of missing values for each variable and sort them in ascending order
sorted_columns = missing_values.sum().sort_values().index

# Reorder the missing_values DataFrame based on the sorted variables
sorted_missing_values = missing_values[sorted_columns]

# Convert the sorted boolean DataFrame of missing values to a numeric format
numeric_missing_values = sorted_missing_values.astype(int)  # 1 for True (missing), 0 for False (not missing)

# Streamlit app starts here
st.title('Flu Shot Learning: Heatmap of Missing Values')

st.write("""
This Streamlit app uses Plotly Express to display Missing Values from the Flu Shot Learning project from Driven Data.
The goal of this project is to predict how likely individuals are to receive their H1N1 and seasonal flu vaccines based upon various features collected in a survey.
The dataset includes characteristics like behavioral responses, opinions, and personal information gathered from respondents. 
         
Whilst doing Exploratory Data Analysis, we noticed some of the features have Missing Values, with implications for how we understand the data. 
Missing Values are an important feature of many real-life datasets in the wild. Missing Values are otherwise known as Not Available (`NA`) or Not A Number (`NaN`) values. 

This heatmap shows the presence of `NaN` values in the dataset according to the column (feature) variables. Do you notice any patterns?
""")

# Increase the figure's height to give more space for y-axis labels
fig_height = max(600, 30 * len(sorted_columns))

fig = px.imshow(numeric_missing_values.T, color_continuous_scale='Viridis',
                labels=dict(x="Rows", y="Columns", color="Missing Values"),
                title="Heatmap",
                height=fig_height)  # Set custom height

# Update layout to improve aesthetics and readability of y-axis labels
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    title_font=dict(size=16, color='white'),
    xaxis=dict(showticklabels=False),
    yaxis=dict(
        tickmode='array',
        tickvals=list(range(len(sorted_columns))),
        ticktext=sorted_columns,
        tickfont=dict(size=10, color='white')  # Adjust font size as needed
    ),
    yaxis_title="Variables",
    xaxis_title="Survey Participants"
)

# Display the figure in the Streamlit app
st.plotly_chart(fig)

st.write("""
We were just about to drop all rows with Missing Values, but after plotting them, we noticed potential patterns in the Missing Values. 
         
We noticed the Missing Values potentially grouped around the following variables:

- `employment_occupation` has 13470 (50.4%) missing values
- `employment_industry` has 13330 (49.9%) missing values
- `health_insurance` has 12274 (46.0%) missing values
- `income_poverty` has 4423 (16.6%) missing values

How might we explain these patterns?
         
This data was taken from a telephone survey. The pattern of Missing Values possibly suggests participants felt uncomfortable answering these questions during the telephone survey. But we don't know!
         
We need to be careful with data where there are many Missing Values. They may give indications about the nature of the data, and give us caution about how we interpret this data.
         
To find out more about how we interpreted this dataset, see [Flu Shot Learning](https://github.com/carecodeconnect/flu-shot-learning)
""")

