import xgboost as xgb
import numpy as np
import random
import pickle
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, mean_squared_error
from sklearn.datasets import load_iris, load_digits, load_boston


def train_xgb(train_data,lbls,idx):
    xgb_model = xgb.XGBClassifier()
    clf = GridSearchCV(xgb_model,
                       {'max_depth': [2, 4, 6, 8],
                        'n_estimators': [20,50,100],},verbose=1)
    clf.fit(train_data, lbls[idx])
    print(clf.best_score_)
    print(clf.best_params_)
    with open('../data/best_bst.pkl', 'wb') as f:
        pickle.dump(clf, f)




if __name__ == "__main__":
    with open('../data/processed_data.pkl', 'rb') as f:
        data, lbls = pickle.load(f)
    # equal fake / real samples
    n_min = np.minimum(np.sum(lbls == 0), np.sum(lbls == 1))
    idx = np.concatenate([random.sample(list(np.where(lbls == 0)[0]), n_min), random.sample(list(np.where(lbls == 1)[0]), n_min)])
    # normalize the data
    train_mean = np.mean(data[idx], axis=0)
    train_std = np.std(data[idx], axis=0)
    train_data = (data[idx] - train_mean) / train_std
    # save normalization params
    # with open('../data/norm_train_params.pkl', 'wb') as f:
    #     pickle.dump([train_mean, train_std],f)
    xgb_model = xgb.XGBClassifier()
    clf = GridSearchCV(xgb_model,
                       {'max_depth': [2, 4, 6],
                        'n_estimators': [50, 100, 200]}, verbose=1)
    clf.fit(train_data, lbls[idx])
    print(clf.best_score_)
    print(clf.best_params_)
    with open('../data/best_bst.pkl', 'wb') as f:
        pickle.dump(clf,f)
