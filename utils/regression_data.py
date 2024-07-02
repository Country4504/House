from sklearn.linear_model import LinearRegression
import numpy as np

def linear_model_main(X_parameter, Y_paramter, predict_value):
    
    regr = LinearRegression()
    
    regr.fit(X_parameter, Y_paramter)
    
    predict_value = np.array([predict_value]).reshape(-1, 1)
    predict_outcome = regr.predict(predict_value)
    
    return predict_outcome
if __name__ == '__main__':
    
    x_data = [[4], [8], [9], [8], [7], [12], [6], [10], [6], [9], [10], [6]]
    y_data = [9, 20, 22, 15, 17, 23, 18, 25, 10, 20, 20, 17]
    
    predict_value = 8    
    predict_outcome = linear_model_main(x_data, y_data, predict_value)[0]
    print('预测结果:', predict_outcome)
