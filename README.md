# Synthetic Database Generator

## A fully functioning database generator that takes in SQL schema and populates the appropriate tables in the database accrording to the user specifications.

This project was created as part of the Rutgers MBS Externship Program's collaboration with CGI Inc. The project is a proof of concept of a technology that is able to generate data for industries/ domain where sensitive informtion is not publically available becuase of privacy laws. Synthetic data generation allows researchers and practitioners to generate data that retains the statistical properties of the original data while removing any identifying information, thus preserving privacy. In certain domains, such as life sciences, obtaining real-world data may be challenging due to various constraints such as cost, time, or limited availability. Synthetic data generation provides a way to create data that simulates real-world scenarios, allowing researchers and practitioners to overcome data scarcity issues.

## Demo
[![Watch the video](https://app.gemoo.com/share/image-annotation/648480079515443200?codeId=M07wAXkN3dboX&origin=imageurlgenerator)](https://youtu.be/-tBHtHAYEsc)

## How to run
1. install required packages from requirements_dev.txt
```
pip install -r requirements.txt
```
2. create "secrets.toml" file in .streamlit folder and save your API key
3. run app.py
```
streamlit run app.py
```
