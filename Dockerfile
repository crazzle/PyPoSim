FROM python:2.7
ADD . /PyPoSim
RUN mkdir /PyPoSim/tslog
RUN chmod 777 -R /PyPoSim
WORKDIR /PyPoSim
EXPOSE 5000
RUN pip install -r requirements.txt
CMD python PyPoSim.py
