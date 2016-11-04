# PyPoSim [![Build Status](https://travis-ci.org/crazzle/PyPoSim.svg?branch=master)](https://travis-ci.org/crazzle/PyPoSim)
A small power plant simulator that can ramp to a certain power level. Great for noisy time-series data generation!

**TO-DO**

[X] Provide Kafka support

[_] Ensure connection to Kafka Broker if Kafka is down on start-up

[X] Log datapoints into a file

[X] Provide REST API


# Getting started
1. Clone the repo
2. Navigate into the PyPoSim folder
3. Install the required dependencies with pip install -r requirements.txt
4. run it with python PyPoSim.py (standard port is 5000)

You can run it alternatively using Docker.

# Play with the simulator
The simulator provides a REST API to create, poll, steere and delete simulated plants.
For stream processing Kafka can be configured accordingly to push datapoints into a topic.

## Add
Plants are added via the **/add** endpoint using the HTTP POST method.
In order to function properly, the body must contain JSON in the following format:

{ "name": "Sample Plant", 	
  "power": 150, 	
  "fluctuation": 10, 	
  "ramp": 15 }

- Name is the name of your plant.
- power is the power this plant generates in KW
- fluctuation is the fluctuation running around the power in percentage
- ramp is the factor the plants ramps up and down per second in KW

The response of this endpoint contains a UID that is used to access the new created simulation.

## Get current power
You can get the current power using **/{UID}**.

## Get master data
You can get the master data using **/masterdata/{UID}**.

## Dispatch
You can dispatch your plant (tell it to ramp to a certain powerlevel) by using 
the **/dispatch/{UID}/{POINT}** endpoint. Point is the new powerlevel your plant should ramp to.
The plant ramps according to the ramp that was specified during creation.

## Delete
To delete a simulator just use **/delete/{UID}**

## MIT Licence
Copyright (c) 2016 Mark Keinhörster

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

