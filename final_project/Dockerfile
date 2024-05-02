FROM python:3.10
RUN apt-get update && apt-get install -y libgl1-mesa-glx
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY /var/lib/jenkins/workspace/OurCar_django/final_project/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]