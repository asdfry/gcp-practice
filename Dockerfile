FROM gcr.io/intnow-gcp-practice/custom-python@sha256:197ab00b51c1ebdb7bdd54531f72e76b41783acbb119a5a92bae998623b0d821

COPY app.py images exam_dump.txt ./

EXPOSE 8501

RUN streamlit run app.py