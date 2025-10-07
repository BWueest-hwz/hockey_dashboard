
# hockey-dashboard.py

# Import necessary libraries
import streamlit as st
import sqlite3 as db
import pandas as pd
import altair as alt
from streamlit.components.v1 import html
from streamlit_navigation_bar import st_navbar

#st_navbar(
#   pages=["Home", "Library", "Tutorials", "Development", "Download"],
#    options={"use_padding": False}
#)

# define league IDs
league_dic = {"Women's League": 'WL', '1. Liga': 'L1', 'U-21 Elit': 'U21', 'National League': 'NL', 'Swiss League': 'SL', 'MySports League': 'ML'}

# Connect to the SQLite database
conn = db.connect('data/hockey_stats.db')

# Set up the page and titles
st.set_page_config(page_title="4-3-2-1", layout="wide")
colA, colB = st.columns([0.75, 8])
with colA:
    st.image('./data/images/fuchs.png', width=125)
with colB:
    st.markdown("### 4-3-2-1: Statistik-Dashboard zum Schweizer Eishockey")
    st.markdown("Dieses Dashboard bringt Analysen und Vorhersagen, welche mithilfe der öffentlich verfügbaren Daten zum Schweizer Eishockey erstellt worden sind. Die Daten stammen vor allem vom Schweizerischen Eishockeyverband (https://www.sihf.ch/de/) und werden von meistens ehrenamtlichen Reporter:innen (merci!) gesammelt. Dies ist ein unentgeltliches und unabhängiges Freizeit-Projekt und hat deshalb keinen Anspruch auf Vollständigkeit, Korrektheit oder Aktualität.")

st.markdown("Zunächst die Analyseebene auswählen:")
tabA, tabB, tabC, tabD = st.tabs(["**Ligen**", "**Teams**", "**Spiele**", "**Spieler:innen**"])
with tabA:
    st.markdown("Hier gibt es den Herfindahl-Index, Gini-Koeffizienten, eine Auswertung der Logos und eine Visualisierung der Google Trends im Zeitverlauf (1 Jahr)")
    # League selection dropdown
    optionL = st.selectbox(
        " ",
        ["Liga auswählen...", "National League", "Women's League", "Swiss League", "MySports League", "1. Liga", "U-21 Elit"]
    )
    if optionL and optionL != "Liga auswählen...":
        with st.expander("**Meisterbrett**", expanded=False):
            league_code = league_dic[optionL]
            # load manual data
            champions = pd.read_excel('./data/4321-manual.xlsx', sheet_name='champions')
            tbl = champions[champions['league_code'] == league_code][['season', 'team_name', 'league_code']].rename(columns={'season': 'Saison', 'team_name': 'Meisterteam', 'league_code': 'league_code'})
            brands = pd.read_sql_query(f"SELECT * FROM {league_code}_teams", conn)
            tbl = pd.merge(tbl, brands[['team_name', 'png_path']], left_on='Meisterteam', right_on='team_name', how='left').drop(columns=['team_name'])
            tbl['png_path'] = tbl['png_path'].fillna('../data/images/empty.png').str.replace('../', './', regex=False)
            colC1, colC2, colC3 = st.columns([2, 5.6, 15])
            with colC1:
                st.markdown("**Saison**")
            with colC2:
                st.markdown("**Meisterteam**")
            with colC3:
                st.markdown("**Platzierung Regular Season**")
            for idx, row in tbl.iterrows():
                colC1, colC2, colC3, colC4 = st.columns([2, 0.6, 5, 15])
                with colC1:
                    saison = str(row["Saison"])
                    prev_year = row["Saison"] - 1 
                    saison = str(prev_year) + '/' + saison
                    st.markdown(saison)
                with colC2:
                    st.image(row["png_path"], width=30)
                with colC3:
                    st.markdown(row["Meisterteam"])
                with colC4:
                    st.markdown(row["Meisterteam"])
        st.expander("**Ausgeglichenheit der Liga**", expanded=False)
        st.expander("**Clublogos**", expanded=False)
        st.expander("**Internet-Aufmerksamkeit**", expanded=False)
        st.expander("**Links zum SIHF und Wikipedia**", expanded=False)
with tabB:
    st.markdown("### Teams")
with tabC:
    st.markdown("### Spiele")
with tabD:
    st.markdown("### Spieler:innen")
