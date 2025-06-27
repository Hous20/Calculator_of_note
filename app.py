
import streamlit as st
import pandas as pd
import plotly.express as px
from parse_grades import parse_grades_from_string

st.set_page_config(page_title="GEMA Note calculator", page_icon="🧮", layout="wide")
st.title("Analyse des Notes")

# Option to paste grades
st.sidebar.header("Entrer vos Notes")
pasted_grades = st.sidebar.text_area("Collez vos notes ici (une matière par bloc de 3 lignes: Nom du cours, Note (Lettre (Valeur numérique)), Coefficient)", height=300)

df = pd.DataFrame()
if pasted_grades:
    df = parse_grades_from_string(pasted_grades)
    if not df.empty:
        st.sidebar.success("Notes parsées avec succès !")
    else:
        st.sidebar.warning("Impossible de parser les notes. Veuillez vérifier le format.")
else:
    st.sidebar.info("Collez vos notes dans la zone de texte ci-dessus pour commencer l'analyse.")


# Main content area
if not df.empty:
    # Overall Metrics
    st.header("Statistiques Générales")

    avg_numerical_grade = df["NumericalGrade"].mean()
    st.metric(label="Moyenne Générale", value=f"{avg_numerical_grade:.2f}")

    st.subheader("Distribution des Notes par Lettre")
    letter_grade_counts = df["LetterGrade"].value_counts().sort_index()
    fig_letter = px.bar(letter_grade_counts, x=letter_grade_counts.index, y=letter_grade_counts.values, labels={
        "x": "Note par Lettre",
        "y": "Nombre d'occurrences"
    }, title="Distribution des Notes par Lettre")
    st.plotly_chart(fig_letter, use_container_width=True)

    st.subheader("Histogramme des Notes Numériques")
    fig_hist = px.histogram(df, x="NumericalGrade", nbins=10, title="Histogramme des Notes Numériques")
    st.plotly_chart(fig_hist, use_container_width=True)

    st.header("Analyse par Cours")
    selected_course = st.selectbox("Sélectionner un Cours", df["Course"].unique())

    if selected_course:
        course_df = df[df["Course"] == selected_course]
        st.subheader(f"Statistiques pour {selected_course}")
        
        if not course_df.empty:
            avg_course_grade = course_df["NumericalGrade"].mean()
            st.metric(label=f"Moyenne pour {selected_course}", value=f"{avg_course_grade:.2f}")

            st.subheader(f"Distribution des Notes par Lettre pour {selected_course}")
            course_letter_grade_counts = course_df["LetterGrade"].value_counts().sort_index()
            fig_course_letter = px.bar(course_letter_grade_counts, x=course_letter_grade_counts.index, y=course_letter_grade_counts.values, labels={
                "x": "Note par Lettre",
                "y": "Nombre d'occurrences"
            }, title=f"Distribution des Notes par Lettre pour {selected_course}")
            st.plotly_chart(fig_course_letter, use_container_width=True)

            st.subheader(f"Histogramme des Notes Numériques pour {selected_course}")
            fig_course_hist = px.histogram(course_df, x="NumericalGrade", nbins=10, title=f"Histogramme des Notes Numériques pour {selected_course}")
            st.plotly_chart(fig_course_hist, use_container_width=True)
        else:
            st.write("Aucune donnée disponible pour ce cours.")
else:
    st.write("Veuillez coller vos notes dans la zone de texte à gauche pour visualiser les analyses.")


