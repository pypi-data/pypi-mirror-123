# 验证函数
def cal_add_1(num1,num2):
    result =  np.mean(num1 +num2)
    return result

# 开始加载环境
import pandas as pd
import numpy as np
# 从这里开始绘制箱线图表示误差的大小
from pandas.plotting import andrews_curves

# 忽略烦人的红色提示
import warnings
warnings.filterwarnings("ignore")

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, cross_val_score,train_test_split,cross_validate, StratifiedKFold
from sklearn.metrics import roc_curve, auc, roc_auc_score,average_precision_score
from sklearn import model_selection

from sklearn.utils import shuffle
import seaborn as sns
sns.set_style("whitegrid")

# 自定义颜色
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# 欢饮语
print("欢迎来到Czy的快乐星球")


# 验证函数
def cal_add_1(num1,num2):
    result =  np.mean(num1 +num2)
    return result


# ============================下面是模型的迭代选择===============================================================
from sklearn.linear_model import RidgeClassifier,LogisticRegressionCV, Perceptron
def LogisticRegressionCV_mdoel(X, Y, cv, score):
    LogisticRegressionCV_auto = LogisticRegressionCV(random_state=0, n_jobs=-1,max_iter=10000)

    # 搜索的参数是para
    param_dict = {"solver": ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
                  "penalty": ['l1', 'l2', 'elasticnet', ],
                  "class_weight": ['none', 'balanced'],
                  "fit_intercept": [True, False],
                  "dual": [True, False],
                  }
    estimator = GridSearchCV(estimator=LogisticRegressionCV_auto, param_grid=param_dict, cv=cv, n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)

    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_



from sklearn.linear_model import SGDClassifier
def SGDClassifier_model(X, Y, cv, score):

    # 首先实例化各个回归方法
    SGDClassifier_auto = SGDClassifier(random_state=0,n_jobs=-1,max_iter=10000)
    param_dict = {"penalty":['l2','elasticnet','l2'],  #
                  "loss":[ 'modified_huber', 'log'], #'hinge'
                  "class_weight":['none','balanced'],
                  "average":[True,False],
                  "warm_start":[True,False],
                  "early_stopping":[True,False],
                  "fit_intercept":[True,False],
                 }
    estimator = GridSearchCV(estimator = SGDClassifier_auto, param_grid=param_dict, cv=cv,n_jobs=-1,scoring = score)
    estimator.fit(X,Y)
    return estimator.best_params_,estimator.best_score_,estimator.best_estimator_


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
def LinearDiscriminantAnalysis_model(X, Y, cv, score):

    # 首先实例化各个判别分析方法
    LinearDiscriminantAnalysis_auto = LinearDiscriminantAnalysis()
    param_dict = {
        "solver": ['svd', 'lsqr', 'eign'],
        "store_covariance": [True, False],
    }
    estimator = GridSearchCV(estimator=LinearDiscriminantAnalysis_auto,
                             param_grid=param_dict,
                             cv=cv,
                             n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_


from sklearn.svm import LinearSVC
def LinearSVC_model(X, Y, cv, score):  # 这就是感知机

    # 首先实例化各个回归方法
    LinearSVC_auto = LinearSVC(random_state=0,max_iter=10000)
    param_dict = {"penalty": ['l2', 'l1'],
                  "loss": ['hinge', 'squared_hinge'],
                  "dual": [True, False],
                  "fit_intercept": [True, False],
                  "class_weight": ['none', 'balanced'],
                  }
    estimator = GridSearchCV(estimator=LinearSVC_auto, param_grid=param_dict, cv=cv, n_jobs=-1, scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_


from sklearn.svm import SVC
def SVC_model(X, Y, cv, score):  # 这就是感知机
    # 首先实例化各个回归方法
    SVC_auto = SVC(random_state=0, probability=True)
    param_dict = {
        "gamma": ['scale', 'auto'],
        "kernel": ['linear', 'poly', 'rbf', 'sigmoid'],  # , 'precomputed' 这个参数对于X有额外的要求
        "shrinking": [True, False],
        "class_weight": ['none', 'balanced'],
    }
    estimator = GridSearchCV(estimator=SVC_auto, param_grid=param_dict, cv=cv, n_jobs=-1, scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_

from sklearn.svm import NuSVC
def NuSVC_model(X, Y, cv, score):   #这就是感知机
    # 首先实例化各个回归方法
    NuSVC_auto = NuSVC(random_state=0,probability=True)
    param_dict = {
                "gamma":['scale','auto'],
                "kernel":[ 'linear', 'poly','rbf', 'sigmoid'] ,     #, 'precomputed' 这个参数对于X有额外的要求
                "shrinking":[True, False],
                "class_weight":['none','balanced'],
                 }
    estimator = GridSearchCV(estimator = NuSVC_auto, param_grid=param_dict, cv=cv,n_jobs=-1,scoring=score)
    estimator.fit(X,Y)
    return estimator.best_params_,estimator.best_score_,estimator.best_estimator_


from sklearn.tree import DecisionTreeClassifier
def DecisionTreeClassifier_model(X, Y, cv, score):
    # 首先实例化各个回归方法
    DecisionTreeClassifier_auto = DecisionTreeClassifier(random_state=0)
    param_dict = {"criterion": ['gini', 'entropy'],
                  "splitter": ['best', 'random'],
                  "max_features": ['auto', 'sqrt', 'log2'],
                  "class_weight": ['none', 'balanced'],
                  }
    estimator = GridSearchCV(estimator=DecisionTreeClassifier_auto, param_grid=param_dict, cv=cv, n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_


# ==
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
DecisionTreeClassifier_auto_ada = DecisionTreeClassifier(random_state=0,criterion= 'gini', max_features='auto', splitter='best')
def AdaBoostClassifier_model(X, Y, cv, score):
    # 首先实例化各个回归方法
    AdaBoostClassifier_auto = AdaBoostClassifier(random_state=0)
    param_dict = {
                 "algorithm":['SAMME', 'SAMME.R']}
    estimator = GridSearchCV(estimator = AdaBoostClassifier_auto, param_grid=param_dict, cv=cv,n_jobs=-1,scoring =score)
    estimator.fit(X,Y)
    return estimator.best_params_,estimator.best_score_,estimator.best_estimator_


from sklearn.ensemble import BaggingClassifier
def BaggingClassifier_model(X, Y, cv, score):
    # 首先实例化各个回归方法
    BaggingClassifier_auto = BaggingClassifier(random_state=0, n_jobs=-1)
    param_dict = {  # "n_estimators":[10,30,50,70,90,110],
        "bootstrap": ["True", "False"],
        "bootstrap_features": ["True", "False"],
        "oob_score": ["True", "False"],
    }
    estimator = GridSearchCV(estimator=BaggingClassifier_auto, param_grid=param_dict, cv=cv, n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_

def GradientBoostingClassifier_model(X, Y, cv, score):
    from sklearn.ensemble import GradientBoostingClassifier
    # 首先实例化各个回归方法
    GradientBoostingClassifier_auto = GradientBoostingClassifier(random_state=0)
    param_dict = {"loss": ["deviance", "exponential"],
                  #                   "n_estimators":[10,30,50,70,90,110],
                  #                  "learning_rate":[0,0.5,1,1.5,2],
                  "criterion": ['friedman_mse', 'mse', "mae"],
                  "max_features": ["auto", "sqrt", "log2"]}
    estimator = GridSearchCV(estimator=GradientBoostingClassifier_auto, param_grid=param_dict, cv=cv, n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_



def RandomForestClassifier_model(X, Y, cv, score):
    from sklearn.ensemble import RandomForestClassifier
    # 首先实例化各个回归方法
    RandomForestClassifier_auto = RandomForestClassifier(random_state=0, n_jobs=-1)
    param_dict = {
        #                   "n_estimators":[10,30,50,70,90,110],
        "criterion": ['gini', 'entropy'],
        "max_features": ["auto", "sqrt", "log2"],
        "class_weight": ['none', 'balanced', "balanced_subsample"],
        "bootstrap": ["True", "False"],
        "oob_score": ["True", "False"],

    }
    estimator = GridSearchCV(estimator=RandomForestClassifier_auto, param_grid=param_dict, cv=cv, n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_


import xgboost as xgb
from xgboost import plot_importance
def xgboost_model(X, Y, cv, score):

    xgboost_auto = xgb.XGBClassifier(random_state=0, n_jobs=1)
    param_dict = {"maximize": ["True", "False"],
                  #                   "n_estimators":[20,40,60,80,100,120],
                  "objective": ['binary:logistic', 'binary:hinge'],  # reg:linear回归时使用
                  }
    estimator = GridSearchCV(estimator=xgboost_auto, param_grid=param_dict, cv=cv, n_jobs=-1, scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_


from sklearn.neighbors import KNeighborsClassifier
def KNeighborsClassifier_model(X, Y, cv, score):
    KNeighborsClassifier_auto = KNeighborsClassifier(n_jobs=1)
    param_dict = {"n_neighbors": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                  "algorithm": ['auto', 'ball_tree', 'kd_tree', 'brute'],
                  "weights": ['uniform', 'distance'],
                  "p": [1, 2],
                  }
    estimator = GridSearchCV(estimator=KNeighborsClassifier_auto, param_grid=param_dict, cv=cv, n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_


from sklearn.neighbors import NearestNeighbors
def NearestNeighbors_model(X, Y, cv, score):
    # 首先实例化各个回归方法
    NearestNeighbors_auto = NearestNeighbors(n_jobs=1)
    param_dict = {
        #                 "radius":[0.5, 1, 1.5, 4],
        "p": [1, 2],
        "algorithm": ['auto', 'ball_tree', 'kd_tree', 'brute'],
    }
    estimator = GridSearchCV(estimator=NearestNeighbors_auto, param_grid=param_dict, cv=cv, n_jobs=-1,
                             scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_


from sklearn.naive_bayes import BernoulliNB
def BernoulliNB_model(X, Y, cv, score):
    # 首先实例化各个回归方法
    BernoulliNB_auto = BernoulliNB()
    param_dict = {"fit_prior": ["True", "False"],
                  "alpha": [-1, 0, 1, 2],
                  }
    estimator = GridSearchCV(estimator=BernoulliNB_auto, param_grid=param_dict, cv=cv, n_jobs=-1, scoring=score)
    estimator.fit(X, Y)
    return estimator.best_params_, estimator.best_score_, estimator.best_estimator_

from sklearn.naive_bayes import GaussianNB
def GaussianNB_model(X, Y, cv, score):
    # 首先实例化各个回归方法
    GaussianNB_auto = GaussianNB()
    param_dict = {
                 }
    estimator = GridSearchCV(estimator = GaussianNB_auto, param_grid=param_dict, cv=cv,n_jobs=-1,scoring = score)
    estimator.fit(X,Y)
    return estimator.best_params_,estimator.best_score_,estimator.best_estimator_


def binary_ROC(X,Y,k,fig_name,score):
    """
    关于名字：binary_ROC 是全部进行二分类的Roc图像绘制
    data: dataframe
    X：   X变量数据的名字
    Y：   label变量的列名
    cv:   表示需要的折叠次数
    :return:   fig 返回ROC图
    """
    # 初始化分层搜索
    cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=0)

    # 调用上文的自动机器学习模型
    LogisticRegressionCV_auto_tmp_1, LogisticRegressionCV_auto_tmp_2, LogisticRegressionCV_auto = LogisticRegressionCV_mdoel(X, Y, cv, score)
    print(LogisticRegressionCV_auto_tmp_1, LogisticRegressionCV_auto_tmp_2, LogisticRegressionCV_auto)

    SGDClassifier_auto_tmp_1, SGDClassifier_auto_tmp_2, SGDClassifier_auto = SGDClassifier_model(X, Y, cv, score)
    print(SGDClassifier_auto_tmp_1, SGDClassifier_auto_tmp_2, SGDClassifier_auto)

    LinearDiscriminantAnalysis_auto_tmp_1, LinearDiscriminantAnalysis_auto_tmp_2, LinearDiscriminantAnalysis_auto = LinearDiscriminantAnalysis_model(X, Y, cv, score)
    print(LinearDiscriminantAnalysis_auto_tmp_1, LinearDiscriminantAnalysis_auto_tmp_2, LinearDiscriminantAnalysis_auto)

    LinearSVC_auto_tmp_1, LinearSVC_auto_tmp_2, LinearSVC_auto = LinearSVC_model(X, Y, cv, score)
    print(LinearSVC_auto_tmp_1, LinearSVC_auto_tmp_2, LinearSVC_auto)

    SVC_auto_tmp_1, SVC_auto_tmp_2, SVC_auto = SVC_model(X, Y, cv, score)
    print(SVC_auto_tmp_1, SVC_auto_tmp_2, SVC_auto)

#     NuSVC_auto_tmp_1, NuSVC_auto_tmp_2, NuSVC_auto = NuSVC_model(X, Y, cv, score)
#     print(NuSVC_auto_tmp_1, NuSVC_auto_tmp_2, NuSVC_auto)

    DecisionTreeClassifier_auto_tmp_1, DecisionTreeClassifier_auto_tmp_2, DecisionTreeClassifier_auto = DecisionTreeClassifier_model(X, Y, cv, score)
    print(DecisionTreeClassifier_auto_tmp_1, DecisionTreeClassifier_auto_tmp_2, DecisionTreeClassifier_auto)

    AdaBoostClassifier_auto_tmp_1, AdaBoostClassifier_auto_tmp_2, AdaBoostClassifier_auto = AdaBoostClassifier_model(X, Y, cv, score)
    print(AdaBoostClassifier_auto_tmp_1, AdaBoostClassifier_auto_tmp_2, AdaBoostClassifier_auto)

    BaggingClassifier_auto_tmp_1, BaggingClassifier_auto_tmp_2, BaggingClassifier_auto = BaggingClassifier_model(X, Y, cv, score)
    print(BaggingClassifier_auto_tmp_1, BaggingClassifier_auto_tmp_2, BaggingClassifier_auto)

    GradientBoostingClassifier_auto_tmp_1, GradientBoostingClassifier_auto_tmp_2, GradientBoostingClassifier_auto = GradientBoostingClassifier_model(X, Y, cv, score)
    print(GradientBoostingClassifier_auto_tmp_1, GradientBoostingClassifier_auto_tmp_2, GradientBoostingClassifier_auto)

    RandomForestClassifier_auto_tmp_1, RandomForestClassifier_auto_tmp_2, RandomForestClassifier_auto = RandomForestClassifier_model(X, Y, cv, score)
    print(RandomForestClassifier_auto_tmp_1, RandomForestClassifier_auto_tmp_2, RandomForestClassifier_auto)

    xgboost_auto_tmp_1, xgboost_auto_tmp_2, xgboost_auto = xgboost_model(X, Y, cv, score)
    print(xgboost_auto_tmp_1, xgboost_auto_tmp_2, xgboost_auto)

    KNeighborsClassifier_auto_tmp_1, KNeighborsClassifier_auto_tmp_2, KNeighborsClassifier_auto = KNeighborsClassifier_model(X, Y, cv, score)
    print(KNeighborsClassifier_auto_tmp_1, KNeighborsClassifier_auto_tmp_2, KNeighborsClassifier_auto)

    NearestNeighbors_auto_tmp_1,  NearestNeighbors_auto_tmp_2, NearestNeighbors_auto = NearestNeighbors_model(X, Y, cv, score)
    print(NearestNeighbors_auto_tmp_1,  NearestNeighbors_auto_tmp_2, NearestNeighbors_auto)

    BernoulliNB_auto_tmp_1, BernoulliNB_auto_tmp_2, BernoulliNB_auto = BernoulliNB_model(X, Y, cv, score)
    print(BernoulliNB_auto_tmp_1, BernoulliNB_auto_tmp_2, BernoulliNB_auto)

    GaussianNB_auto_tmp_1, GaussianNB_auto_tmp_2, GaussianNB_auto = GaussianNB_model(X, Y, cv, score)
    print(GaussianNB_auto_tmp_1, GaussianNB_auto_tmp_2, GaussianNB_auto)

    colors = [
        '#00429d', '#2f5aa8', '#4774b4', '#5c8ebf', '#6fa9ca', '#83c4d5',
        '#99e0e0', '#c0f8ec', '#fccbe5', '#f7b6cc', '#f1a1b4', '#ea8c9c',
        '#e27786', '#d96171', '#cf4969'
    ]

    #     创建model字典，其中的最佳模型就是取自上文的model
    algorithm_models = [
        LogisticRegressionCV_auto,
        #         RidgeClassifier_auto,    'RidgeClassifier' object has no attribute 'predict_proba'
        #         Perceptron_auto,  'RidgeClassifier' object has no attribute 'predict_proba'
        SGDClassifier_auto,
        LinearDiscriminantAnalysis_auto,
        #         QuadraticDiscriminantAnalysis_auto,
        #         LinearSVC_auto, # 'LinearSVC' object has no attribute 'predict_proba'
        SVC_auto,
#         NuSVC_auto,
        DecisionTreeClassifier_auto,
        #         ExtraTreeClassifier_auto,
        AdaBoostClassifier_auto,
        BaggingClassifier_auto,
        GradientBoostingClassifier_auto,
        RandomForestClassifier_auto,
        xgboost_auto,
        KNeighborsClassifier_auto,
        #         NearestNeighbors_auto, # 'NearestNeighbors' object has no attribute 'predict'
        GaussianNB_auto,
        BernoulliNB_auto,
    ]

    #     创建名字列表
    algorithm_names = [
        "LogisticRegression",
        #         "RidgeClassifier",
        #         "Perceptron",
        "SGDClassifier",
        "LinearDA",
        #         "QuadraticDA",
        #         "LinearSVC",
        "SVC",
#         "NuSVC",
        "DecisionTree",
        #         "ExtraDecisionTree",
        "AdaBoost",
        "Bagging",
        "GTBoost",
        "RandomForest",
        "XGBoost",
        "KNeighbors",
        #         "NearestNeighbors"
        "BernoulliNB",
        "GaussianNB"
    ]

    X_train_, X_test_, y_train, y_test = model_selection.train_test_split(
        X, Y,
        test_size=0.2,
        random_state=0,
        stratify=Y,
        shuffle=True  # y_imbalance 是 label的那一列
    )
    print(y_test)

    transfer = StandardScaler()
    X_train_0 = transfer.fit_transform(X_train_)
    X_test_0 = transfer.transform(X_test_)


    # 下面开始绘图
    fig = plt.figure(figsize=(10, 10), dpi=300)
    for (name, method, colorname) in zip(algorithm_names, algorithm_models,colors):
        method.fit(X_train_0, y_train)
        # y_test_preds = method.predict(X_test_0)  # 好像是无效计算
        y_test_predprob = method.predict_proba(X_test_0)[:, 1]
        fpr, tpr, thresholds = roc_curve(y_test, y_test_predprob, pos_label=1)

        plt.plot(fpr,
                 tpr,
                 lw=5,
                 label='{} (AUC={:.3f})'.format(name, auc(fpr, tpr)),
                 color=colorname)

    plt.plot([0, 1], [0, 1], '--', lw=5, color='grey')
    plt.axis('square')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel('False Positive Rate', fontsize=15)
    plt.ylabel('True Positive Rate', fontsize=15)
    plt.title('ROC Curve of Auto_ML ', fontsize=20)

    if fig_name == False:
        fig_name = "ROC"

    plt.legend(loc='lower right',
               fontsize=10,
               title=fig_name,
               shadow=True,
               fancybox=True,
               ncol=2)

    ## 添加局部放大图
    inset_ax = fig.add_axes([0.57, 0.40, 0.3, 0.3],facecolor="white")  # 这是局部放大图四个角的位置
    for (name, method, colorname) in zip(algorithm_names, algorithm_models,colors):
        method.fit(X_train_0, y_train)
        # y_test_preds = method.predict(X_test_0)
        y_test_predprob = method.predict_proba(X_test_0)[:, 1]
        fpr, tpr, thresholds = roc_curve(y_test, y_test_predprob, pos_label=1)
        inset_ax.plot(fpr,
                      tpr,
                      lw=5,
                      label='{} (AUC={:.3f})'.format(name, auc(fpr, tpr)),
                      color=colorname)
        inset_ax.set_xlim([-0.01, 0.3])
        inset_ax.set_ylim([0.7, 1.01])
        inset_ax.grid()

    plt.show()

    return fig

# 下面是对应的模型参数比较====================================================================
def auto_model(X, Y, k,score):
    """
    说明:
        X ,Y :DataFrame 形式的数据
        k 是几折分层验证的参数
    :return Auc_data, Acc_data, Recall_data, Precision_data 四个评判指标的Dataframe

    """
    cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=0)

    # 调用上文的自动机器学习模型
    LogisticRegressionCV_auto_tmp_1, LogisticRegressionCV_auto_tmp_2, LogisticRegressionCV_auto = LogisticRegressionCV_mdoel(X, Y, cv, score)
    print(LogisticRegressionCV_auto_tmp_1, LogisticRegressionCV_auto_tmp_2, LogisticRegressionCV_auto)

    SGDClassifier_auto_tmp_1, SGDClassifier_auto_tmp_2, SGDClassifier_auto = SGDClassifier_model(X, Y, cv, score)
    print(SGDClassifier_auto_tmp_1, SGDClassifier_auto_tmp_2, SGDClassifier_auto)

    LinearDiscriminantAnalysis_auto_tmp_1, LinearDiscriminantAnalysis_auto_tmp_2, LinearDiscriminantAnalysis_auto = LinearDiscriminantAnalysis_model(X, Y, cv, score)
    print(LinearDiscriminantAnalysis_auto_tmp_1, LinearDiscriminantAnalysis_auto_tmp_2, LinearDiscriminantAnalysis_auto)

    LinearSVC_auto_tmp_1, LinearSVC_auto_tmp_2, LinearSVC_auto = LinearSVC_model(X, Y, cv, score)
    print(LinearSVC_auto_tmp_1, LinearSVC_auto_tmp_2, LinearSVC_auto)

    SVC_auto_tmp_1, SVC_auto_tmp_2, SVC_auto = SVC_model(X, Y, cv, score)
    print(SVC_auto_tmp_1, SVC_auto_tmp_2, SVC_auto)

#     NuSVC_auto_tmp_1, NuSVC_auto_tmp_2, NuSVC_auto = NuSVC_model(X, Y, cv, score)
#     print(NuSVC_auto_tmp_1, NuSVC_auto_tmp_2, NuSVC_auto)

    DecisionTreeClassifier_auto_tmp_1, DecisionTreeClassifier_auto_tmp_2, DecisionTreeClassifier_auto = DecisionTreeClassifier_model(X, Y, cv, score)
    print(DecisionTreeClassifier_auto_tmp_1, DecisionTreeClassifier_auto_tmp_2, DecisionTreeClassifier_auto)

    AdaBoostClassifier_auto_tmp_1, AdaBoostClassifier_auto_tmp_2, AdaBoostClassifier_auto = AdaBoostClassifier_model(X, Y, cv, score)
    print(AdaBoostClassifier_auto_tmp_1, AdaBoostClassifier_auto_tmp_2, AdaBoostClassifier_auto)

    BaggingClassifier_auto_tmp_1, BaggingClassifier_auto_tmp_2, BaggingClassifier_auto = BaggingClassifier_model(X, Y, cv, score)
    print(BaggingClassifier_auto_tmp_1, BaggingClassifier_auto_tmp_2, BaggingClassifier_auto)

    GradientBoostingClassifier_auto_tmp_1, GradientBoostingClassifier_auto_tmp_2, GradientBoostingClassifier_auto = GradientBoostingClassifier_model(X, Y, cv, score)
    print(GradientBoostingClassifier_auto_tmp_1, GradientBoostingClassifier_auto_tmp_2, GradientBoostingClassifier_auto)

    RandomForestClassifier_auto_tmp_1, RandomForestClassifier_auto_tmp_2, RandomForestClassifier_auto = RandomForestClassifier_model(X, Y, cv, score)
    print(RandomForestClassifier_auto_tmp_1, RandomForestClassifier_auto_tmp_2, RandomForestClassifier_auto)

    xgboost_auto_tmp_1, xgboost_auto_tmp_2, xgboost_auto = xgboost_model(X, Y, cv, score)
    print(xgboost_auto_tmp_1, xgboost_auto_tmp_2, xgboost_auto)

    KNeighborsClassifier_auto_tmp_1, KNeighborsClassifier_auto_tmp_2, KNeighborsClassifier_auto = KNeighborsClassifier_model(X, Y, cv, score)
    print(KNeighborsClassifier_auto_tmp_1, KNeighborsClassifier_auto_tmp_2, KNeighborsClassifier_auto)

    NearestNeighbors_auto_tmp_1, NearestNeighbors_auto_tmp_2, NearestNeighbors_auto = NearestNeighbors_model(X, Y, cv, score)
    print(NearestNeighbors_auto_tmp_1, NearestNeighbors_auto_tmp_2, NearestNeighbors_auto)

    BernoulliNB_auto_tmp_1, BernoulliNB_auto_tmp_2, BernoulliNB_auto = BernoulliNB_model(X, Y, cv, score)
    print(BernoulliNB_auto_tmp_1, BernoulliNB_auto_tmp_2, BernoulliNB_auto)

    GaussianNB_auto_tmp_1, GaussianNB_auto_tmp_2, GaussianNB_auto = GaussianNB_model(X, Y, cv, score)
    print(GaussianNB_auto_tmp_1, GaussianNB_auto_tmp_2, GaussianNB_auto)

    colors = [
        '#00429d', '#2f5aa8', '#4774b4', '#5c8ebf', '#6fa9ca', '#83c4d5',
        '#99e0e0', '#c0f8ec', '#fccbe5', '#f7b6cc', '#f1a1b4', '#ea8c9c',
        '#e27786', '#d96171', '#cf4969'
    ]

    #     创建model字典
    algorithm_models = [
        LogisticRegressionCV_auto,
        #         RidgeClassifier_auto,    'RidgeClassifier' object has no attribute 'predict_proba'
        #         Perceptron_auto,  'RidgeClassifier' object has no attribute 'predict_proba'
        SGDClassifier_auto,
        LinearDiscriminantAnalysis_auto,
        #         QuadraticDiscriminantAnalysis_auto,
        #         LinearSVC_auto, # 'LinearSVC' object has no attribute 'predict_proba'
        SVC_auto,
#         NuSVC_auto,
        DecisionTreeClassifier_auto,
        #         ExtraTreeClassifier_auto,
        AdaBoostClassifier_auto,
        BaggingClassifier_auto,
        GradientBoostingClassifier_auto,
        RandomForestClassifier_auto,
        xgboost_auto,
        KNeighborsClassifier_auto,
        #         NearestNeighbors_auto, # 'NearestNeighbors' object has no attribute 'predict'
        GaussianNB_auto,
        BernoulliNB_auto,
    ]

    #     创建名字列表
    algorithm_names = [
        "LogisticRegression",
        #         "RidgeClassifier",
        #         "Perceptron",
        "SGDClassifier",
        "LinearDA",
        #         "QuadraticDA",
        #                 "LinearSVC",
        "SVC",
#         "NuSVC",
        "DecisionTree",
        #         "ExtraDecisionTree",
        "AdaBoost",
        "Bagging",
        "GTBoost",
        "RandomForest",
        "XGBoost",
        "KNeighbors",
        #         "NearestNeighbors"
        "BernoulliNB",
        "GaussianNB"
    ]

    # 指定存储结果的字典表 行是模型名字，列是次数
    tmp_1 = np.zeros((len(algorithm_names), 5))
    Auc_data = pd.DataFrame(tmp_1, index=algorithm_names, columns=range(5))
    tmp_2 = np.zeros((len(algorithm_names), 5))
    Acc_data = pd.DataFrame(tmp_2, index=algorithm_names, columns=range(5))
    tmp_3 = np.zeros((len(algorithm_names), 5))
    Recall_data = pd.DataFrame(tmp_3, index=algorithm_names, columns=range(5))
    tmp_4 = np.zeros((len(algorithm_names), 5))
    Precision_data = pd.DataFrame(tmp_4, index=algorithm_names, columns=range(5))

    score_funcs = ['accuracy', 'precision', 'recall', 'roc_auc']

    for (name, method) in zip(algorithm_names, algorithm_models):
        #         print(name)
        scores = cross_validate(method,
                                X,
                                Y,
                                scoring=score_funcs,
                                cv=cv,  # 直接嫁接 上面定义的 cv
                                return_estimator=True)

        model_auc = scores['test_accuracy']
        model_acc = scores['test_roc_auc']
        model_recall = scores['test_recall']
        model_precision = scores['test_precision']

        for i in range(5):
            Auc_data[i].loc[name] = model_auc[i]
            Acc_data[i].loc[name] = model_acc[i]
            Recall_data[i].loc[name] = model_recall[i]
            Precision_data[i].loc[name] = model_precision[i]

    return Auc_data, Acc_data, Recall_data, Precision_data


def estimator_violion(df1,df2,fig_name):
    """
    :param df1: 小提琴左侧的函数
    :param df2: 小提琴右侧的函数
    :return:  小提琴图
    """
    colors = [
        '#00429d', '#2f5aa8', '#4774b4', '#5c8ebf', '#6fa9ca', '#83c4d5',
        '#99e0e0', '#c0f8ec', '#fccbe5', '#f7b6cc', '#f1a1b4', '#ea8c9c',
        '#e27786', '#d96171', '#cf4969'
    ]

    # 处理A数据
    aa = df1.T
    aa.describe()
    # 处理B数据
    bb = df2.T
    bb.describe()
    # 处理合并数据
    AA = aa.melt()
    AA.columns = ["Model_A", "ROC"]
    df_A = AA
    BB = bb.melt()
    BB.columns = ["Model_B", "ACC"]
    df_B = BB
    df_AB = pd.concat([df_A, df_B], axis=1)
    df_AB_fig = df_AB.drop("Model_B", axis=1)
    df_AB_fig.columns = ["Model", "ROC", "ACC"]
    df_AB_fig_1 = pd.melt(df_AB_fig, id_vars="Model", value_name="Value")

    # 下面开始绘图
    pal2 = sns.color_palette(['#6fa9ca', '#ea8c9c'])
    sns.set_palette(pal2)
    sns.palplot(pal2)
    fig = plt.figure(figsize=(20, 10), dpi=300)
    sns.violinplot(x="Model",
                   y="Value",
                   hue="variable",
                   data=df_AB_fig_1,
                   split=True, inner="quartile",
                   )
    # Decoration
    if fig_name == False:
        fig_name = 'Violinplot of Auto ML'
    plt.title(fig_name, fontsize=22)
    ax = plt.gca()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=12)
    ax.set_xlabel(ax.get_xlabel(), fontsize=17)  # get函数得到原来默认的参数
    ax.set_ylabel(ax.get_ylabel(), fontsize=17)
    ax.legend(fontsize=20)
    plt.show()

    return fig

