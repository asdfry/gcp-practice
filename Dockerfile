FROM gcr.io/intnow-gcp-practice/custom-python:3.9-slim

COPY app.py images exam_dump.txt ./

EXPOSE 8501

RUN streamlit run app.py