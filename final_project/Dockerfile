# 기본 이미지로 Python 3.9를 사용합니다.
FROM python:3.10

# libGL.so.1 라이브러리를 설치합니다.
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 호스트의 현재 디렉토리에 있는 requirements.txt를 컨테이너 내 /app 디렉토리로 복사합니다.
COPY ./requirements.txt /app/

# pip를 이용하여 필요한 Python 패키지들을 설치합니다.
RUN pip install -r requirements.txt

# 호스트의 현재 디렉토리에 있는 모든 파일을 컨테이너 내 /app 디렉토리로 복사합니다.
COPY . /app/


# 컨테이너 내에서 사용할 포트를 엽니다. Django 기본 포트는 8000입니다.
EXPOSE 8000

# Django 서버를 실행합니다.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]