import os
import os.path
import time

import pickle
import pandas as pd
from pathlib import Path
from sklearn.pipeline import make_pipeline
import sklearn.externals
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

import sys
from mylibrary.data_handling import Features


def export_model(dataframe=None, your_name=None, mode=None):
    # Path 설정
    md_dir = str(Path(__file__).parent.parent)
    ml_dir = str(Path(__file__).parent)

    # 데이터
    data = dataframe
    features_col = Features().featrues_col()
    target_col = Features().target_col()

    # 학습 데이터, 훈련 데이터
    X = data[features_col]
    y = data[target_col]

    # 학습 훈련 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

    ## 데이터의 불균형한 정도
    train = pd.concat([X_train, y_train], axis=1)
    scale_weight_0 = int(train[target_col].value_counts()[0])
    scale_weight_1 = int(train[target_col].value_counts()[1])

    ## 초기 모델링
    clf_rf = make_pipeline(
        RandomForestClassifier(n_jobs=-1, random_state=10)
    )
    clf_rf.fit(X_train, y_train);

    ## 하이퍼 파라미터 튜닝
    param_tuning = {
    'randomforestclassifier__class_weight' : ['balanced', {0:scale_weight_0, 1:scale_weight_1}],
    'randomforestclassifier__n_estimators': [10, 50, 100],
    'randomforestclassifier__max_depth': [1, 5, 10],
    'randomforestclassifier__min_samples_leaf' : [5, 10, 15],
    'randomforestclassifier__max_features': [0.3, 0.5, 0.7] # max_features
    }

    clf_rf_rmd = GridSearchCV(estimator = clf_rf,
                            param_grid = param_tuning,                        
                            scoring = 'accuracy',
                            cv = 3,
                            n_jobs = -1,
                            verbose = 1)

    ## 리모델링                        
    clf_rf_rmd.fit(X_train, y_train);
    joblib.dump(clf_rf_rmd, md_dir + f'/my_app/rf_model/rcmd_{your_name}.pkl')

    # 모델 저장(첫 학습, 재 학습 구분)
    if mode is None: # 모델이 없는 경우
        joblib.dump(clf_rf_rmd, md_dir + f'/my_app/rf_model/rcmd_{your_name}.pkl')
    else: # 모델이 있는 경우
        if os.path.isfile(md_dir + f'/my_app/rf_model/rcmd_{your_name}.pkl'):
            os.rename(md_dir + f'/my_app/rf_model/rcmd_{your_name}.pkl', md_dir + f'/my_app/rf_model/rcmd_{your_name}_{time.time()}.pkl')
        joblib.dump(clf_rf_rmd, md_dir + f'/my_app/rf_model/rcmd_{your_name}.pkl')

if __name__ == "__main__":
    try:
        export_model()
    except:
        pass