import xgboost as xgb
from Predictor import Predictor
from FeatureEngineering import *


class XGBoostPredictor(Predictor):

    def __init__(self, train, test, params={}, name='XGBoost'):
        super().__init__(train, test, params, name=name)
        self.model = xgb.XGBClassifier(**params)

    def set_params(self, params):
        self.model = xgb.XGBClassifier(**params)

    def fit(self, params=None, train=None):
        """
        A function that trains the predictor on the given dataset. Optionally accepts a set of parameters
        """

        # If parameters are supplied, override constructor one's
        if params is not None:
            self.set_params(params)

        if train is None:
            self.preprocess()
            train, _ = self.split()

        y_train = train['target'].values
        x_train = train.drop('target', axis=1).values
        self.model.fit(x_train, y_train)

    def predict(self, x_val):
        if not self.model:
            raise ValueError("The predictor has not been trained yet")

        prediction = self.model.predict_proba(x_val.as_matrix())[:, 1]
        return prediction

if __name__ == "__main__":

    # Test that the classifier works
    train = pd.read_csv('data/train.csv')
    test = pd.read_csv('data/test.csv')


    ##### RUN XGBOOST
    print("\nSetting up data for XGBoost ...")

    params = {
        'learning_rate': 0.02,
        'max_depth': 4,
        'subsample': 0.9,
        'n_estimators': 1500,
        'colsample_bytree': 0.9,
        'objective': 'binary:logistic',
        'min_child_weight': 10,
        'silent': 1
    }

    model = XGBoostPredictor(train, test, params)
    # model.create_submission(params)

    # # Tune Model
    # print("Tuning XGBoost...")
    # tuning_params = {
    #     'learning_rate': [0.05],
    #     'silent': [1],
    #     'max_depth': [5],
    #     'subsample': [1],
    #     'reg_lambda': [0.8, 0.9],
    #     'n_jobs': [8],
    #     'n_estimators': [100, 200]
    # }
    # optimal_params, optimal_score = model.tune(tuning_params)

    # Train the model using the best set of parameters found by the gridsearch
    print("\nTraining XGBoost ...")
    model.fit(params)

    print("\nEvaluating model...")
    gini = model.evaluate()

    print("\n##########")
    print("GINI score is: ", gini)
    print("##########")