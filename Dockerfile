FROM python:2.7
ADD . /PyPoSim
WORKDIR /PyPoSim
EXPOSE 5001
RUN pip install -r requirements.txt
CMD python PyPoSim.py
