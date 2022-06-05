FROM gcr.io/intnow-gcp-practice/custom-python:3.9-slim

COPY app.py images exam_dump.txt key.json ./

ENV GOOGLE_APPLICATION_CREDENTIALS=/key.json