FROM python:3.12-slim

# setting container working dir to /app
WORKDIR /app

# install dependencies, don't save package files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# now clone all to all
COPY . .

# gimme my port
EXPOSE 8000

# start django:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]