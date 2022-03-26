FROM python
ADD teleg_bot_cam.py .
ADD settings.py .
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "teleg_bot_cam.py"]