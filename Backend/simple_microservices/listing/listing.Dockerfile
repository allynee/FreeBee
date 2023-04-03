FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

# Start the app with uvicorn
CMD ["uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]
