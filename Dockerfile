FROM gcr.io/intnow-gcp-practice/custom-python:3.9-slim

# 트리거 사용 시
COPY app.py images exam_dump.txt ./

# 트리거 미사용 시
# COPY app.py images exam_dump.txt key.json ./
# ENV GOOGLE_APPLICATION_CREDENTIALS=/key.json