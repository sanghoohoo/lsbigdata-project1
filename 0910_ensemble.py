from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bagging_model = BaggingClassifier(DecisionTreeClassifier(),
                                  n_estimator = 50, # 모델 갯수
                                  max_samples = 100, # 표본 크기
                                  n_jobs = -1, random_state = 42)

# bagging_model.fit(X_train, y_train)

from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(n_estimators=50,
                                  max_leaf_node=16,
                                  n_jobs=-1, random_state=42)
# rf_model.fit(X_train, y_train)