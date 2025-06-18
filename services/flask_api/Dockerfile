FROM python:3.12

WORKDIR /app
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app/menus

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
# COPY . .
COPY src/ /app/src/
COPY migrations/ /app/migrations/
COPY requirements.txt /app/
COPY wsgi.py /app/

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0"]

