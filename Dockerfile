FROM python:2.7
ADD . /PyPoSim
WORKDIR /PyPoSim
RUN pip install -r requirements.txt
CMD python PyPoSim.py