import pickle
import pandas as pd


def predict(p1, p2, p3, p4, p5, p6, p7, p8):
    f = open('Recom_Pre/pkl/pred_group.pkl', 'rb')
    deci_tree = pickle.load(f)
    f.close()
    
    dict = {'1':[p2], '2':[p3], '3':[p4], '4':[p5], '5':[p6], '6':[p7], '7':[p8]}
    X_test = pd.DataFrame(dict)
    y_pred = deci_tree.predict(X_test)
    #print('ทำนายผลการสอบกลางาค คุุณจะอยู่ในเกณฑ์', y_pred)
    return y_pred[0]
