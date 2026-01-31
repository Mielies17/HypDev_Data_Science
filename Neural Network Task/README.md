# Neural Network task: Slogan Generator and Classifier

### Please note that this notebook must be run in Google Colab

## Description
 In this project, a Long Short-Term Memory (LSTM) model is trained to generate slogans for businesses based on their industry and another LSTM model is trained to use a given slogan and predict the industry. The two were combined by feeding a specific industry into the generator model and feeding the generated slogan into the classified model to see if the classifier model would correctly predict the specific industry. The results and differences were evaluated.

## Files
- neural-network_task.ipynb: Jupyter Notebook file in which LSTM models were trained for the generator and classifier
- slogan-valid.csv: CSV file containing different industries with their associated slogans as well as other features