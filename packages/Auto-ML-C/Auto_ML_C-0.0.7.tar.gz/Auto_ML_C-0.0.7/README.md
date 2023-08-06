**Auto_ML_C **

# Illustrate：

​	这是崔连山和小伙伴们的机器学习拓展包，代有浓厚的社会主义开源分享精神，极富创造力和战斗力。在这里让我们为他们鼓掌 :clinking_glasses:

## Spend

测试集数据位置：{Example}

如果全流程,源码的速度是 Fast_Example.ipynb是 38s

| 函数【有感知机版本】 | 耗时   | 函数【无感知机版本】 | 耗时  |
| -------------------- | ------ | -------------------- | ----- |
| 以下数据在i9-9750H   |        | 12核上测试           |       |
| binary_ROC(X,Y,5,)   | 566.51 | 也就是去掉NuSVC      | 52.63 |
| auto_model(X,Y,5)    | 556.12 |                      | 52.60 |

## Request_install

可以参考学习当前目录下的环境备份：Auto_ML_C.yaml

主要是涉及到的软件如下：

| Package          | 最低版本——待检测 |
| ---------------- | ---------------- |
| python=3.8.10    |                  |
| seaborn=0.11.2   |                  |
| pandas=1.3.3     |                  |
| matplotlib=3.4.2 |                  |
| numpy=1.20.3     |                  |
| py-xgboost=1.4.0 |                  |
|                  |                  |



# Content:

​    该包是基于Sklearn，imblance等机器学习拓展包之上的Package，共计划分为两个部分，

- 建模类

  1. binary_classfication.py

     内部可用函数如下

     | 函数名                                    | 功能                                    | 返回值                                                |
     | ----------------------------------------- | --------------------------------------- | ----------------------------------------------------- |
     | cal_add_1(num1,num2):wave:                | 简单的欢迎函数                          | num1,num2                                             |
     | LogisticRegressionCV_mdoel(X, Y,cv)       |                                         |                                                       |
     | SGDClassifier_model(X,Y,cv)               |                                         |                                                       |
     | LinearDiscriminantAnalysis_model(X, Y,cv) |                                         |                                                       |
     | LinearSVC_model(X, Y,cv)                  |                                         |                                                       |
     | SVC_model(X, Y,cv)                        |                                         |                                                       |
     | NuSVC_model(X,Y,cv)                       |                                         |                                                       |
     | DecisionTreeClassifier_model(X,Y,cv)      |                                         |                                                       |
     | AdaBoostClassifier_model(X,Y,cv)          |                                         |                                                       |
     | BaggingClassifier_model(X, Y,cv)          |                                         |                                                       |
     | GradientBoostingClassifier_model(X, Y,cv) |                                         |                                                       |
     | RandomForestClassifier_model(X, Y,cv)     |                                         |                                                       |
     | xgboost_model(X, Y,cv)                    |                                         |                                                       |
     | KNeighborsClassifier_model(X, Y,cv)       |                                         |                                                       |
     | NearestNeighbors_model(X, Y,cv)           |                                         |                                                       |
     | BernoulliNB_model(X, Y,cv)                |                                         |                                                       |
     | GaussianNB_model(X,Y,cv)                  |                                         |                                                       |
     | 下面是新增函数                            |                                         |                                                       |
     | binary_ROC(X,Y,k,fig_name)                | 绘制标量超参数搜索下最佳的ROC           | fig                                                   |
     | auto_model(X, Y, k)                       | 模型的标量超参数搜索结果                | Auc_data, Acc_data, <br />Recall_data, Precision_data |
     | estimator_violion(df1,df2,fig_name)       | 为auto_model结果的Dataframe绘制小提琴图 | fig                                                   |

     

  2. binary_classfication_ws.py

     这是为了速度考虑，舍弃占用90%时间的NuSVC函数的函数

  3. 多分类函数
     


# ConTact

VX：Cuizy13390906310_ic

QQ：1776228595

E-mail：1776228595@qq.com

GitHub：地址待填写

