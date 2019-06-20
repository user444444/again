FROM python:3
ADD . /time_off
WORKDIR /time_off
#COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .
#CMD ["python","app.py"]





