FROM python:3
WORKDIR /app
ADD static/ ./static
ADD templates ./templates
ADD app.py .
ADD app.yaml .
ADD start.py .
ADD requirements.txt .
ENV PYTHONUNBUFFERED=1
RUN python -m pip install -r requirements.txt
ENTRYPOINT ["python", "start.py"]