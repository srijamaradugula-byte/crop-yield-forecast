FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# use real data if present, otherwise fall back to synthetic sample data, then train
RUN [ -f data/yield_data.csv ] || python -m src.generate_sample_data
RUN python -m src.train
ENV PORT=8000
EXPOSE 8000
CMD uvicorn app.api:app --host 0.0.0.0 --port ${PORT}
