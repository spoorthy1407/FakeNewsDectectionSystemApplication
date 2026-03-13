FROM python:3.10-slim

WORKDIR /app

COPY . /app


RUN pip install --no-cache-dir -r req.txt

EXPOSE 5000
EXPOSE 8501
CMD [ "bash", "-c", "python app.py & streamlit run dashboard/admin.py --server.port 8501 --server.address 0.0.0.0"]
