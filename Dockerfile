FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
# ENV HF_HOME='/home/mapr/indeco-jobs/indeco_ai/quickteller_rag/'
# ENV STREAMLIT_CONFIG='/home/mapr/indeco_jobs/indeco_ai/quickteller_rag/project_isw/app/.streamlit/'
# ENV HOME='/home/mapr/indeco_jobs/indeco_ai/quickteller_rag/'

CMD ["streamlit", "run", "app.py"]
