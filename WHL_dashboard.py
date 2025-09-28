
# WHL_dashboard.py

# Import necessary libraries
import streamlit as st
import sqlite3 as db
import pandas as pd
import altair as alt

# Set up the page and titles
st.set_page_config(page_title="WHL Stats", layout="wide")
st.title("WHL Stats")
st.markdown("Statistical dashboard of the Womens' Hockey League Switzerland")

# Load data from the SQLite database
conn = db.connect('data/WHL_stats.db')
teams = pd.read_sql_query("SELECT * FROM teams", conn)
points_ema = pd.read_sql_query("SELECT * FROM points_ema", conn)
wins_ema = pd.read_sql_query("SELECT * FROM wins_ema", conn)
ppe_ema = pd.read_sql_query("SELECT * FROM ppe_ema", conn)
pke_ema = pd.read_sql_query("SELECT * FROM pke_ema", conn)
scoring_ema = pd.read_sql_query("SELECT * FROM scoring_ema", conn)
defense_ema = pd.read_sql_query("SELECT * FROM goals_alloed_ema", conn)
spectators_ema = pd.read_sql_query("SELECT * FROM spectators_ema_home", conn)
turnover_ema = pd.read_sql_query("SELECT * FROM turnover_ema_home", conn)
conn.close()

# Team selection dropdown
option = st.selectbox(
    " ",
    ["Bitte ein Team auswählen..."] + teams['team_name'].tolist()
)

# Display team information and statistics in separate tabs
if option and option != "Bitte ein Team auswählen...":
    # Display team logo and name
    col1, col2 = st.columns([1, 3])
    with col1:
        img_path = teams.loc[teams['team_name'] == option, 'png_url'].values[0]
        st.image(img_path, width=150)
    with col2:
        st.markdown(f"# {option}")

    # Create tabs for different statistics
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Wins", "Points", "Powerplay", "Penaltykill", "Scoring", "Defense", "Attendance", "Turnover"])
    with tab1:
        st.markdown(f"**Gewinnwahrscheinlichkeit über die bisherige Spielzeit in der WHL (max=100 Prozent)**")
        wins_data = wins_ema[wins_ema['Team'] == option]
        wins_data["Date"] = pd.to_datetime(wins_data["Date"])
        wins_data = wins_data[['YearMonthDay', 'EMA']]
        wins_data['EMA'] = wins_data['EMA'] * 100  # Convert to percentage
        chart = alt.Chart(wins_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title='Exponentially Weighted Average', scale=alt.Scale(domain=[0, 100])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EWA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)
    with tab2:
        st.markdown(f"**Geschätzte Punkte über die bisherige Spielzeit in der WHL (max=3 Punkte)**")
        points_data = points_ema[points_ema['Team'] == option]
        points_data["Date"] = pd.to_datetime(points_data["Date"])
        points_data = points_data[['YearMonthDay', 'EMA']]
        chart = alt.Chart(points_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title="Exponentially Weighted Average", scale=alt.Scale(domain=[0, 3])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EWA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)
    with tab3:
        st.markdown(f"**Powerplay-Effizienz über die bisherige Spielzeit in der WHL (max=100 Prozent)**")
        ppe_data = ppe_ema[ppe_ema['Team'] == option]
        ppe_data["Date"] = pd.to_datetime(ppe_data["Date"])
        ppe_data = ppe_data[['YearMonthDay', 'EMA']]
        ppe_data['EMA'] = ppe_data['EMA'] * 100  # Convert to percentage
        chart = alt.Chart(ppe_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title='Exponentially Weighted Moving Average', scale=alt.Scale(domain=[0, 60])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EMA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)
    with tab4:
        st.markdown(f"**Penaltykill-Effizienz über die bisherige Spielzeit in der WHL (max=100 Prozent)**")
        pke_data = pke_ema[pke_ema['Team'] == option]
        pke_data["Date"] = pd.to_datetime(pke_data["Date"])
        pke_data = pke_data[['YearMonthDay', 'EMA']]
        pke_data['EMA'] = pke_data['EMA'] * 100  # Convert to percentage
        chart = alt.Chart(pke_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title='Exponentially Weighted Moving Average', scale=alt.Scale(domain=[40, 100])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EMA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)
    with tab5:
        st.markdown(f"**Scoring-Produktivität über die bisherige Spielzeit in der WHL**")
        scoring_data = scoring_ema[scoring_ema['Team'] == option]
        scoring_data["Date"] = pd.to_datetime(scoring_data["Date"])
        scoring_data = scoring_data[['YearMonthDay', 'EMA']]
        chart = alt.Chart(scoring_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title='Exponentially Weighted Moving Average', scale=alt.Scale(domain=[0, 20])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EMA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)
    with tab6:
        st.markdown(f"**Defensive Instabilität über die bisherige Spielzeit in der WHL**")
        defense_data = defense_ema[defense_ema['Team'] == option]
        defense_data["Date"] = pd.to_datetime(defense_data["Date"])
        defense_data = defense_data[['YearMonthDay', 'EMA']]
        chart = alt.Chart(defense_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title='Exponentially Weighted Moving Average', scale=alt.Scale(domain=[0, 10])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EMA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)
    with tab7:
        st.markdown(f"**Zuschauerandrang über die bisherige Spielzeit in der WHL**")
        spectators_data = spectators_ema[spectators_ema['Team'] == option]
        spectators_data["Date"] = pd.to_datetime(spectators_data["Date"])
        spectators_data = spectators_data[['YearMonthDay', 'EMA']]
        chart = alt.Chart(spectators_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title='Exponentially Weighted Moving Average', scale=alt.Scale(domain=[0, 2500])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EMA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)
    with tab8:
        st.markdown(f"**Spielerwechsel über die bisherige Spielzeit in der WHL in Prozent**")
        turnover_data = turnover_ema[turnover_ema['Team'] == option]
        turnover_data["Date"] = pd.to_datetime(turnover_data["Date"])
        turnover_data = turnover_data[['YearMonthDay', 'EMA']]
        turnover_data['EMA'] = turnover_data['EMA'] * 100  # Convert to percentage
        chart = alt.Chart(turnover_data).mark_line().encode(
            x=alt.X('YearMonthDay', title='Spieltage', sort='ascending'),
            y=alt.Y('EMA', title='Exponentially Weighted Moving Average', scale=alt.Scale(domain=[0, 40])),
            tooltip=[
                alt.Tooltip('YearMonthDay', title='Spieltag'),
                alt.Tooltip('EMA', title='EMA', format=".1f")
            ]
        )
        st.altair_chart(chart, use_container_width=True)