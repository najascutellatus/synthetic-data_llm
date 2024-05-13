# Synthetic Database Generator

## A fully functioning database generator that takes in SQL schema and populates the appropriate tables in the database accrording to the user specifications.

The project is a proof of concept of a technology that is able to generate data for industries/ domain where sensitive informtion is not publically available becuase of privacy laws. Synthetic data generation allows researchers and practitioners to generate data that retains the statistical properties of the original data while removing any identifying information, thus preserving privacy. In certain domains, such as life sciences, obtaining real-world data may be challenging due to various constraints such as cost, time, or limited availability. Synthetic data generation provides a way to create data that simulates real-world scenarios, allowing researchers and practitioners to overcome data scarcity issues. Created as part of the Rutgers MBS Externship Program's collaboration with CGI Inc.

## Demo
[![Watch the video](https://cdn.discordapp.com/attachments/810824356774805505/1239422700389404754/image.png?ex=6642ddd7&is=66418c57&hm=cb93cfbf0b09748ad4fe43b0426108fb9b7b88b7adf0de0c8e7e156649d0f8a6&)](https://youtu.be/-tBHtHAYEsc)

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
