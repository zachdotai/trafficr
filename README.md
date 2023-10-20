# trafficr

### Context

This repo contains code that can be used to setup a batch job in Python to collect the average speeds on a predefined interval across major roads in Kuwait. 

The average speed information can be used to estimate the traffic flow across the respective roads which can be helpful in conducting research of urban traffic flow and its impact on the environment.

The project includes the Python script that can be used as a cronjob with your Google Maps API to collect the average speeds and store in a NoSQL database (Firebase) service, the script that extracts the data from the NoSQL database to convert into csv format for data manipulation, modelling, and analysis afterwards, the requirements file for the scripts to work on your local machine, and the data collected.

### Table of Contents

1. [Instructions](#instructions)
2. [File Descriptions](#files)
3. [Licensing](#licensing)

### Instructions  <a name="installation"></a>
1. Run the following commands in the project's root directory to set up project.

    - To download project requirements
        `pip install -r requirements.txt`
    - To create a file to save your environment variables (including your API keys)
        `vim keys.env`
    - Open your environment file and add your API keys accordingly
        `touch keys.env`

2. Go to `src` directory by running the following command in the terminal: `cd src`

3. Run the batch job script for one time collection app using the following command in the terminal: `python3 run.py`

4. Run the formatting script for one time processing of the data collected from the previous step using the following command in the terminal: `python3 process_data.py`

### File Descriptions  <a name="files"></a>

```
.
├── README.md
├── src                                 -- Code for running the batch job
│   ├── run.py                              -- Python script to run the batch job
│   └── process_data.py                     -- Python script to process the data collected by the run.py script
└── data                                -- Collected data from Google Maps API
    ├── traffic_flow.json                   -- Preprocessed data obtained through the API
    └── processed_data.csv                  -- Google Maps data after being processed


### Licensing  <a name="licensing"></a>
Feel free to use the code here as you would like but please don't forget to mention our project!

