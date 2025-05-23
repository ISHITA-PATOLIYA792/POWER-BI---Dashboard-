# 🕵️‍♀️ Crime Dashboard - 2022 Analysis 📊

Welcome to the **Crime Dashboard Project**, a powerful and visually compelling tool built using **Power BI** and **Streamlit** for analyzing crime data from the year **2022**. This dashboard helps uncover trends, identify hotspots, and provide insightful crime statistics to aid better decision-making.

> 🚨 Dive into the data, explore crime patterns, and visualize incidents with just a few clicks!

---

## 🌟 Dashboard Preview

📷 Here’s a glimpse of the interactive dashboard:

![Dashboard Screenshot](https://github.com/ISHITA-PATOLIYA792/POWER-BI---Dashboard-/blob/main/images/Screenshot%202025-05-23%20121514.png)
![Dashboard Screenshot]([images/Screenshot 2025-05-23 121530.png](https://github.com/ISHITA-PATOLIYA792/POWER-BI---Dashboard-/blob/main/images/Screenshot%202025-05-23%20121530.png))
![Dashboard Screenshot]([images/Screenshot 2025-05-23 121540.png](https://github.com/ISHITA-PATOLIYA792/POWER-BI---Dashboard-/blob/main/images/Screenshot%202025-05-23%20121540.png))

---

## 🚀 Key Features

- 🎨 **Modern Custom Color Theme** (Orange / Peach / Black)
- 📑 **Sidebar Navigation**  
  → Main Dashboard  
  → Locality-Based Analysis  
  → Crime Type Exploration
- 🧠 **Filters**: Crime Type, Location, Arrest Status, Domestic Involvement, Month, Date Range
- 📊 **KPI Cards**:  
  - Total Crimes  
  - Arrests  
  - Domestic Crimes
- 🍩 **Charts**:  
  - Donut Chart: Top 5 Crime Types  
  - Bar Chart: Top 5 Locations by Crime
- 📈 **Time Series**: Line Chart for Monthly & Quarterly Trends
- 🌳 **Hierarchical View**: Treemap of Top 5 Wards
- 🗺️ **Map Integration**: Crime Hotspot Visualization *(if lat/lon available)*

---

## 📁 Files Included

| File/Folder Name                 | Description                                  |
|----------------------------------|----------------------------------------------|
| `crime_data.csv`                | Raw dataset exported from Power BI           |
| `crime_rate_analysis_2022.pbix`| Interactive Power BI dashboard file          |
| `images/`                       | Folder containing dashboard screenshots      |

---

## 📦 Setup & Usage

To run the **Streamlit** version locally:

```bash
pip install streamlit pandas matplotlib
streamlit run app.py
