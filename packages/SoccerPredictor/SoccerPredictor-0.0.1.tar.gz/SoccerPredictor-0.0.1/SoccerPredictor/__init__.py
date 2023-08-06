import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import pickle


class Prediction:
    def __init__(self, data, model):
        self.soccer_data = data
        self.classifier = model

    def soccer_result(self):
        # feature selection
        self.new_df = self.soccer_data.drop(self.soccer_data.iloc[:, 0:23], axis=1,
                                            inplace=False)  # Drop a number of categorical features after performing feature correlation
        self.new_df.drop(['type'], axis=1, inplace=True)  # Drop the type column
        self.new_df.dropna(axis=0, inplace=True)  # Drop any row with missing values

        # Obtain target class from the score column
        self.new_df['outcome'] = self.new_df['score_fulltime'].apply(lambda i: 1 if i[0] > i[-1] else (2 if i[0] < i[-1] else 0))
        self.new_df.drop(['score_fulltime'], axis=1, inplace=True)  # Drop the score_fulltime column

        # Removing % sign
        columns_to_check = self.new_df.columns
        self.new_df[columns_to_check] = self.new_df[columns_to_check].replace({r'\%': ''}, regex=True)

        # Converting the feature values with % to floating values
        self.new_df.iloc[:, 0:21] = self.new_df.iloc[:, 0:21].astype('float') / 100.0

        # Remove more rows with missing values
        self.new_df.dropna(axis=0, inplace=True)

        self.X = self.new_df.drop('outcome', axis=1)
        self.y = self.new_df['outcome'].copy()
        # Convert the input and target vectors to numpy arrays
        self.X = self.X.values
        self.y = self.y.values

        # Predict on the test set
        self.y_pred = self.classifier.predict(self.X)
        # Obtain the testing accuracy
        self.test_acc = accuracy_score(self.y, self.y_pred)
        # Obtain the classification report
        self.clf_report = classification_report(self.y, self.y_pred, target_names=['Draw', 'Home Win', 'Away Win'])

        #Print Results
        print('Model Prediction Accuracy:', self.test_acc)
        print('\n')
        print('Model Classification Report \n', self.clf_report)
