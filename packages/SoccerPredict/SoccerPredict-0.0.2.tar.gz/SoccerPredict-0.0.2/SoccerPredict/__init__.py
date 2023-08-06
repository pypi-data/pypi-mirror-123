import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
import pickle


class Prediction:
    def __init__(self, data, model):
        self.soccer_data = data
        self.classifier = model

    def data_transform(self):
        # saving the match between two teams
        self.home_team = self.soccer_data['homeTeam_team_name']
        self.home_team = self.home_team.values.tolist()
        self.away_team = self.soccer_data['awayTeam_team_name']
        self.away_team = self.away_team.values.tolist()

        self.match = []

        for i in range(len(self.home_team)):
            self.match_played = "{} vs {}".format(self.home_team[i], self.away_team[i])
            self.match.append(self.match_played)

        self.soccer_data['match'] = self.match

        self.soccer_data.set_index('match', inplace=True)

        # feature selection
        self.new_df = self.soccer_data.drop(self.soccer_data.iloc[:, 0:23], axis=1,
                                            inplace=False)  # Drop a number of categorical features after performing feature correlation
        self.new_df.dropna(axis=0, inplace=True)  # Drop any row with missing values

        # Obtain target class from the score column
        self.new_df['outcome'] = self.new_df['score_fulltime'].apply(
            lambda i: 1 if i[0] > i[-1] else (2 if i[0] < i[-1] else 0))
        self.new_df.drop(['score_fulltime'], axis=1, inplace=True)  # Drop the score_fulltime column

        # Removing % sign
        columns_to_check = self.new_df.columns
        self.new_df[columns_to_check] = self.new_df[columns_to_check].replace({r'\%': ''}, regex=True)

        # Converting the feature values with % to floating values
        self.new_df.iloc[:, 0:21] = self.new_df.iloc[:, 0:21].astype('float') / 100.0

        # Remove more rows with missing values
        self.new_df.dropna(axis=0, inplace=True)

        # Split Data into feature vector and target
        self.fixture = self.new_df.index.copy()
        self.X = self.new_df.drop('outcome', axis=1)
        self.y = self.new_df['outcome'].copy()
        # Convert the input and target vectors to numpy arrays
        self.X = self.X.values
        self.y = self.y.values

    def match_prob(self):
        self.y_pred2 = self.classifier.predict_proba(self.X)
        self.outcome = pd.DataFrame(data=self.y_pred2, index=self.fixture,
                                    columns=['winning_percent_draw', 'winning_percent_home', 'winning_percent_away'])
        pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.expand_frame_repr', False)

    def match_predict(self):
        # Predict on the test set
        self.y_pred = self.classifier.predict(self.X)
        # Obtain the testing accuracy
        self.test_acc = accuracy_score(self.y, self.y_pred)
        # Obtain Prediction Error
        self.pred_error = 1 - self.test_acc
        # Obtain the classification report
        self.clf_report = classification_report(self.y, self.y_pred, target_names=['Draw', 'Home Win', 'Away Win'])
        # Get the confusion matrix: Showing the correctness and misclassifications made by the models
        self.conf = confusion_matrix(self.y, self.y_pred)

    def match_result(self):
        print('Match Prediction Probabilities:\n')
        print(self.outcome)
        print('\n')
        print('Model Prediction Accuracy:', self.test_acc)
        print('Model Prediction Error:', self.pred_error)
        print('\n')
        print('Model Classification Report: \n', self.clf_report)
        print('Model Confusion Matrix: \n', self.conf)