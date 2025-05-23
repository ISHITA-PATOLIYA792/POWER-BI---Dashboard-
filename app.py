import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# color palette
MAIN_COLOR = "#f7a58a"
ACCENT_COLOR = "#2d2d2d"
BG_COLOR = "#1a1a1a"
TEXT_COLOR = "#fff"

# page config
st.set_page_config(page_title="crime dashboard", layout="wide")

# load data
def load_data():
    df = pd.read_csv("crime_data.csv", parse_dates=["Date"])
    df.columns = df.columns.str.strip()
    df["Year"] = pd.to_datetime(df["Date"], errors='coerce').dt.year
    df["Month"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime('%b')
    df["Day"] = pd.to_datetime(df["Date"], errors='coerce').dt.day
    return df

df = load_data()

# sidebar navigation
page = st.sidebar.radio("navigate", ["main", "locality based", "type exploration"])

# sidebar filters
st.sidebar.header("filters")
crime_types = st.sidebar.multiselect("primary type", options=df["Primary Type"].unique(), default=df["Primary Type"].unique())
locations = st.sidebar.multiselect("location", options=df["Location"].unique(), default=df["Location"].unique())
arrest_status = st.sidebar.multiselect("arrest", options=df["Arrest"].unique(), default=df["Arrest"].unique())
domestic_status = st.sidebar.multiselect("domestic", options=df["Domestic"].unique(), default=df["Domestic"].unique())
months = st.sidebar.multiselect("month", options=df["Month"].unique(), default=df["Month"].unique())
date_range = st.sidebar.date_input("date range", [df["Date"].min(), df["Date"].max()])

# filter data
df_filt = df[
    (df["Primary Type"].isin(crime_types)) &
    (df["Location"].isin(locations)) &
    (df["Arrest"].isin(arrest_status)) &
    (df["Domestic"].isin(domestic_status)) &
    (df["Month"].isin(months)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# main page
if page == "main":
    st.title("crime rate analysis (2022)")
    col1, col2, col3 = st.columns(3)
    col1.metric("no. of crime", len(df_filt))
    col2.metric("total no. of arrest", df_filt[df_filt["Arrest"] == True].shape[0])
    col3.metric("total no. of domestic", df_filt[df_filt["Domestic"] == True].shape[0])

    # donut chart - top 5 types of crime
    top_types = df_filt["Primary Type"].value_counts().nlargest(5).reset_index()
    fig1 = px.pie(top_types, names="index", values="Primary Type", hole=0.5, color_discrete_sequence=[MAIN_COLOR, ACCENT_COLOR, "#e57373", "#bdb76b", "#a0522d"])
    fig1.update_layout(paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
    st.plotly_chart(fig1, use_container_width=True)

    # bar chart - top 5 location wise crime
    top_locs = df_filt["Location"].value_counts().nlargest(5).reset_index()
    top_locs.columns = ["Location", "Count"]
    fig2 = px.bar(top_locs, x="Location", y="Count", color="Location", title="top 5 location wise crime", color_discrete_sequence=[MAIN_COLOR, ACCENT_COLOR, "#e57373", "#bdb76b", "#a0522d"])
    fig2.update_layout(paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
    st.plotly_chart(fig2, use_container_width=True)

    # line chart - crime by month & quarter
    timeline_df = df_filt.groupby(df_filt["Date"].dt.to_period("M")).size().reset_index(name='Crimes')
    timeline_df["Date"] = timeline_df["Date"].astype(str)
    fig3 = px.line(timeline_df, x="Date", y="Crimes", title="no. of crime by month & quarter", color_discrete_sequence=[MAIN_COLOR])
    fig3.update_layout(paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
    st.plotly_chart(fig3, use_container_width=True)

    # raw data
    with st.expander("show raw data"):
        st.dataframe(df_filt)

# locality based page
elif page == "locality based":
    st.title("crime rate analysis (2022) - locality based")
    # donut chart - top 5 block
    if "Block" in df_filt.columns:
        top_blocks = df_filt["Block"].value_counts().nlargest(5).reset_index()
        fig4 = px.pie(top_blocks, names="index", values="Block", hole=0.5, color_discrete_sequence=[MAIN_COLOR, ACCENT_COLOR, "#e57373", "#bdb76b", "#a0522d"])
        fig4.update_layout(paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
        st.plotly_chart(fig4, use_container_width=True)
    # bar chart - top 3 crime by quarter/month
    if "Quarter" in df_filt.columns:
        top3 = df_filt[df_filt["Primary Type"].isin(df_filt["Primary Type"].value_counts().nlargest(3).index)]
        qtr_df = top3.groupby(["Quarter", "Primary Type"]).size().reset_index(name="Count")
        fig5 = px.area(qtr_df, x="Quarter", y="Count", color="Primary Type", title="no. of top 3 crime by quarter & month", color_discrete_sequence=[MAIN_COLOR, ACCENT_COLOR, "#e57373"])
        fig5.update_layout(paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
        st.plotly_chart(fig5, use_container_width=True)
    # treemap - top 5 wards
    if "Ward" in df_filt.columns:
        top_wards = df_filt["Ward"].value_counts().nlargest(5).reset_index()
        fig6 = px.treemap(top_wards, path=["index"], values="Ward", color="Ward", color_continuous_scale=[MAIN_COLOR, ACCENT_COLOR])
        fig6.update_layout(paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
        st.plotly_chart(fig6, use_container_width=True)
    # map - crime hotspot
    if "Latitude" in df_filt.columns and "Longitude" in df_filt.columns:
        st.markdown("### crime hotspot & type of crime")
        st.map(df_filt[["Latitude", "Longitude"]].dropna())

# type exploration page
elif page == "type exploration":
    st.title("crime rate analysis (2022) - type exploration")
    # kpis
    col1, col2, col3 = st.columns(3)
    col1.metric("no. of arrest recorded", df_filt[df_filt["Arrest"] == True].shape[0])
    col2.metric("no. of primary crimes", df_filt.shape[0])
    col3.metric("sum of domestic crimes", df_filt[df_filt["Domestic"] == True].shape[0])
    # bar chart - top 5 type of crime with highest arrest
    if "Primary Type" in df_filt.columns:
        arrest_by_type = df_filt[df_filt["Arrest"] == True]["Primary Type"].value_counts().nlargest(5).reset_index()
        arrest_by_type.columns = ["Primary Type", "Arrest Count"]
        fig7 = px.bar(arrest_by_type, x="Primary Type", y="Arrest Count", color="Primary Type", title="top 5 type of crime where highest arrest is done", color_discrete_sequence=[MAIN_COLOR, ACCENT_COLOR, "#e57373", "#bdb76b", "#a0522d"])
        fig7.update_layout(paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
        st.plotly_chart(fig7, use_container_width=True)
    # line chart - arrest and domestic by district
    if "District" in df_filt.columns:
        by_district = df_filt.groupby("District").agg(sum_arrest=("Arrest", "sum"), sum_domestic=("Domestic", "sum")).reset_index()
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(x=by_district["District"], y=by_district["sum_arrest"], mode='lines+markers', name='arrest', line=dict(color=MAIN_COLOR)))
        fig8.add_trace(go.Scatter(x=by_district["District"], y=by_district["sum_domestic"], mode='lines+markers', name='domestic', line=dict(color=ACCENT_COLOR)))
        fig8.update_layout(title="arrest and domestic arrests by district", paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
        st.plotly_chart(fig8, use_container_width=True)
    # table - type, count, sum of arrest
    if "Primary Type" in df_filt.columns:
        type_table = df_filt.groupby("Primary Type").agg(count_primary=("Primary Type", "count"), sum_arrest=("Arrest", "sum")).reset_index()
        st.dataframe(type_table)

# raw data
with st.expander("show raw data"):
    st.dataframe(df_filt)
