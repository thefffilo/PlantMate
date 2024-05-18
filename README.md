# PlantMate

## Overview
This repository contains the project that me and my team developed during an hackaton.

The main idea was to create an AI agent that can access some sensors data api and execute python code to analyze the data.

There are 3 main parts: 
- nodejs backend
- streamlit user interface
- rivet project (low-code Visual AI Programming Environment)

## Code
The rivet-example-main folder contains frontend and backend applications. 
These two applications were adapted from the Rivet tutorial available [here](https://github.com/Ironclad/rivet-example).
The frontend is used only for debugging (it was already in the tutorial).
How to run the backend: 
```
npm install
export OPENAIKEY=[openai api key]
npm run start-server
```

The real frontend interface is made with Streamlit. It's found in the interfaccia.py file.
To run the frontend: 
```
pip install -r requirements.txt
streamlit run interfaccia.py
```

### Disclaimer:
This project is just a MVP, there are a lot of bugs and all the code is ugly and not efficient.
We also assumed that the python code generated by the llm is completely secure and cannot cause any damage, therefore we didn't implement any security measure.
