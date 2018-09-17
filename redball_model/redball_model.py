#data format
def NemoCfgMongoClient():
    #user = "root"
    #pw   = "bYKH2Utx47Nw4P"
    host = "0.0.0.0"
    port = 27017
    from pymongo import MongoClient
    uri = "mongodb://%s:%s" % (host, port)
    client = MongoClient(uri)
    return client
client = NemoCfgMongoClient()
X = []
Y = []
def in_data_format(doc):
    #float(doc["home_value"]),float(doc["guest_value"]),
    basic_info = [float(doc["home_water"]),float(doc["guest_water"]),float(doc["win_rate"]),float(doc["draw_rate"]),float(doc["lost_rate"])]
    home_team_info = [float(doc["home_last_win"]),float(doc["home_last_draw"]),float(doc["home_last_lost"]),float(doc["home_last_goal"]),float(doc["home_last_gain"])]
    guest_team_info = [float(doc["guest_last_win"]),float(doc["guest_last_draw"]),float(doc["guest_last_lost"]),float(doc["guest_last_goal"]),float(doc["guest_last_gain"])]
    
    basic_info.extend(home_team_info)
    basic_info.extend(guest_team_info)
    return basic_info
def out_data_format(doc):
    result = doc["score"].split(":")
    home_score = int(result[0])
    guest_socre = int(result[1])
    if home_score>guest_socre:
        return 3
    elif home_score==guest_socre:
        return 1
    else:
        return 0
#,{"game_type":{"$in":["美职足","巴甲","阿甲","比甲","英冠","英甲","墨超","瑞超","法乙","俄超","欧罗巴","欧冠","法甲","英超","荷甲","葡超","德乙","荷乙","西甲","意甲","苏超","德甲"]}}    
#"$and":[{"home_value":{"$ne":"0"}},{"guest_value":{"$ne":"0"}}]
#train data prepare
for doc in client.data_500wan.detail_games.find({"score":{"$exists":True}}):
    try:
        X.append(in_data_format(doc))
        Y.append(doc)
    except Exception as e:
        print e
        continue
print len(X)
print len(Y)
#train & test data split
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size = 0.8,random_state=2) #train 80%, test 20%

from  sklearn import preprocessing  
scaler= preprocessing.StandardScaler().fit(X_train) 
X_train=scaler.transform(X_train) 
X_test=scaler.transform(X_test)

#train & verify
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='sgd',activation='relu', alpha=1e-5,
                    hidden_layer_sizes=(200,100,100), random_state=1)

Y_train_result = [out_data_format(doc) for doc in Y_train]
clf = clf.fit(X_train, Y_train_result)
Y_test_result = [out_data_format(doc) for doc in Y_test]
print( clf.score(X_test, Y_test_result))

#save model
from sklearn.externals import joblib
from sklearn import svm
import os
 
# os.chdir("workspace/model_save")
X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)
joblib.dump(clf, "redball_model.m")