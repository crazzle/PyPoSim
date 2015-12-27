# PyPoSim
A small power plant simulator that can ramp to a certain power level. Great for noisy time-series data generation!

# Getting started
1. Clone the repo
2. Navigate into the PyPoSim folder
3. Install the required dependencies with pip install -r requirements.txt
4. run it with gunicorn PyPoSim:app (standard port is 8000)

# Play with the simulator
The simulator provides a REST API to create, poll, steere and delete simulated plants.

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
