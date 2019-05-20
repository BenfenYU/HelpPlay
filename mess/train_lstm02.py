

import numpy as np
import matplotlib.pyplot as plt
import os,math
import tensorflow as tf

csv_file_name = './data/BuzzLightyearPlanetRescue.csv'
rnn_unit = 10  # 隐层数量
input_size =2 
output_size = 1
time_step = 1
lr = 0.0006  # 学习率
epochs = 500
originalData = []

sample_mean = np.array([70.76278837,  1.29588766, 34.13239719]) 
sample_std = np.array([41.18567931 ,0.45644075 ,17.66665945])

# 输入层、输出层权重、偏置
weights = {
    # 从指定的正太分布中去出一定个数的值，第一个参数为shape，即返回的随机数的维度，别的参数如均值方差来限定分布
    # tf.Variable是声明一个图变量，但没初始化
    'in': tf.Variable(tf.random_normal([input_size, rnn_unit])),
    'out': tf.Variable(tf.random_normal([rnn_unit, 1]))
    }
biases = {
    # 常量张量
    'in': tf.Variable(tf.constant(0.1, shape=[rnn_unit, ])),
    'out': tf.Variable(tf.constant(0.1, shape=[1, ]))
    }

def read_csv():
    with open(csv_file_name,'r') as fp:
        for line in fp:
            data = line.split(',')
            natureNum = int(data[0])
            before = int(data[1])
            holiday = int(data[2])

            originalData.append([natureNum,before,holiday])

    length = len(originalData)
    dataToTest =originalData[math.floor(0.75*length):]
    dataToTrain = originalData[:math.floor(0.75*length)]

    return dataToTrain,dataToTest

# 获取训练集
def get_train_data(train_end,batch_size=1, time_step=1,train_begin=0 ):
    batch_index = []
    data_train = dataToTrain[train_begin:train_end]
    data_train = np.array(data_train).astype(np.float)
    normalized_train_data = (
        data_train-np.mean(data_train, axis=0))/np.std(data_train, axis=0)  # 标准化
    #print(np.mean(data_train, axis=0),np.std(data_train, axis=0))
    train_x, train_y = [], []  # 训练集
    for i in range(len(normalized_train_data)-time_step):
        if i % batch_size == 0:
            batch_index.append(i)
        x = normalized_train_data[i:i+time_step, :-1]
        y = normalized_train_data[i:i+time_step, -1, np.newaxis]
        train_x.append(x.tolist())
        train_y.append(y.tolist())
    batch_index.append((len(normalized_train_data)-time_step))
    
    return batch_index, train_x, train_y

def lstm(X):
    # tf.shape获取尺寸维度，返回一个tensor
    # 这里直接定义俩size，X只包含数据即可，不用携带其他信息
    batch_size = 1#tf.shape(X)[0]
    time_step = 1#tf.shape(X)[1]
    # 获取两个图变量
    w_in = weights['in']
    b_in = biases['in']
    input = tf.reshape(X, [-1, input_size])  # 需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
    # 俩参数的矩阵相乘
    input_rnn = tf.matmul(input, w_in)+b_in
    # 将tensor转成3维，作为lstm cell的输入
    input_rnn = tf.reshape(input_rnn, [-1, time_step, rnn_unit])
    # 一个最基本的LSTM类，
    cell = tf.contrib.rnn.BasicLSTMCell(rnn_unit)
    print(type(cell))
    # 初始化
    init_state = cell.zero_state(batch_size, dtype=tf.float32)

    # dynamic_rnn递归神经网络（RNN）的函数,cell是LSTM、GRU等的记忆单元，输出就是每个cell的输出，state
    # 为最后一个cell的输出状态，LSTM的话输出状态为一个元组(C,h)
    output_rnn, final_states = tf.nn.dynamic_rnn(
        cell, input_rnn, initial_state=init_state, dtype=tf.float32)
    output = tf.reshape(output_rnn, [-1, rnn_unit])
    w_out = weights['out']
    b_out = biases['out']
    # 再相乘，输出
    pred = tf.matmul(output, w_out)+b_out
    
    return pred, final_states

def train_lstm( train_data,batch_size=1, time_step=1,epochs=epochs, train_begin=0):
    train_end = len(train_data)
    # 这是个占位符张量，给多大的变量占位置
    X = tf.placeholder(tf.float32, shape=[None, time_step, input_size])
    Y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
    batch_index, train_x, train_y = get_train_data(train_end,batch_size, time_step, train_begin)
    # 为这个上下文中的变量的命名，即name
    with tf.variable_scope("sec_lstm"):
        pred, _ = lstm(X)
    # 沿着tensor的某一维度，计算元素的平均值。由于输出tensor的维度比原tensor的低，这类操作也叫降维
    loss = tf.reduce_mean(
        # 对参数内所有元素进行平方操作
        tf.square(tf.reshape(pred, [-1])-tf.reshape(Y, [-1])))
    # 此函数是Adam优化算法：是一个寻找全局最优点的优化算法，引入了二次方梯度校正。相比于基础SGD算法，1.不容易陷于局部优点。2.速度更快
    train_op = tf.train.AdamOptimizer(lr).minimize(loss)
    saver = tf.train.Saver(tf.global_variables(), max_to_keep=15)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(epochs):  # 这个迭代次数，可以更改，越大预测效果会更好，但需要更长时间
            for step in range(len(batch_index)-1):
                print(train_x[batch_index[
                                    step]:batch_index[step+1]])
                _, loss_ = sess.run([train_op, loss], feed_dict={X: train_x[batch_index[
                                    step]:batch_index[step+1]], Y: train_y[batch_index[step]:batch_index[step+1]]})
            if (i+1)%50==0 and batch_index != 0:
                print("Number of epochs:", i+1, " loss:", loss_)
                print("model_save: ", saver.save(sess, './HelpPlay/models/tf_lstm/lstm02_BuzzLightyearPlanetRescue'))
        # 在Linux下面用 'model_save2/modle.ckpt'
        print("The train has finished")

def prediction(test_data,time_step=20):
    X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
    mean,std,test_x,test_y=get_test_data(test_data,time_step,test_begin=0)
    with tf.variable_scope("sec_lstm",reuse=tf.AUTO_REUSE):
        pred,_=lstm(X)
    #saver=tf.train.Saver(tf.global_variables())
    # 读取图的信息
    saver = tf.train.import_meta_graph('./HelpPlay/models/tf_lstm/lstm02_BuzzLightyearPlanetRescue.meta')
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        #参数恢复
        module_file = tf.train.latest_checkpoint('./HelpPlay/models/tf_lstm/')
        saver.restore(sess, module_file)
        test_predict=[]
        for step in range(len(test_x)-1):
            prob=sess.run(pred,feed_dict={X:[test_x[step]]})
            predict=prob.reshape((-1))
            test_predict.extend(predict)
        test_y=np.array(test_y)*std[-1]+mean[-1]
        test_predict=np.array(test_predict)*std[-1]+mean[-1]
        acc=np.average(np.abs(test_predict-test_y[:len(test_predict)]))  #mean absolute error
        print("The MAE of this predict:",acc)
        #以折线图表示结果
        plt.figure(figsize=(24,8))
        plt.plot(list(range(len(test_predict))), test_predict, color='b',label = 'prediction')
        plt.plot(list(range(len(test_y))), test_y,  color='r',label = 'origin')
        plt.legend(fontsize=24)
        plt.show()

def test_prediction(time_step=20):
    X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
    test_x=test_get_test_data(time_step,test_begin=0)
    mean,std,_,_=get_test_data(time_step,test_begin=0)
    with tf.variable_scope("sec_lstm",reuse=True):
        pred,_=lstm(X)
    saver=tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        #参数恢复
        module_file = tf.train.latest_checkpoint('model_save')
        saver.restore(sess, module_file)
        test_predict=[]
        for step in range(len(test_x)-1):
            prob=sess.run(pred,feed_dict={X:[test_x[step]]})
            predict=prob.reshape((-1))
            test_predict.extend(predict)
        test_predict=np.array(test_predict)*std[4]+mean[4]
        #以折线图表示结果
        plt.figure(figsize=(24,8))
        plt.plot(list(range(len(test_predict))), test_predict, color='b',label = 'prediction')
        plt.legend(fontsize=24)
        plt.show()
        return test_predict

# 获取测试集
def test_get_test_data(data_test,time_step=1,test_begin=0):
    data_test = data[test_begin:]
    mean = np.mean(data_test, axis=0)
    std = np.std(data_test, axis=0)
    normalized_test_data = (data_test-mean)/std  # 标准化
    size = (len(normalized_test_data)+time_step-1)//time_step  # 有size个sample
    test_x = []
    for i in range(size-1):
        x = normalized_test_data[i*time_step:(i+1)*time_step, :4]        
        test_x.append(x.tolist())    
    test_x.append((normalized_test_data[(i+1)*time_step:, :4]).tolist())
    return test_x

def get_test_data(data,time_step=1,test_begin=0):
    data_test = data[test_begin:]
    mean = np.mean(data_test, axis=0)
    std = np.std(data_test, axis=0)
    normalized_test_data = (data_test-mean)/std  # 标准化
    size = (len(normalized_test_data)+time_step-1)//time_step  # 有size个sample
    test_x, test_y = [], []
    for i in range(size-1):
        x = normalized_test_data[i*time_step:(i+1)*time_step, :-1]
        y = normalized_test_data[i*time_step:(i+1)*time_step, -1]
        test_x.append(x.tolist())
        test_y.extend(y)
    test_x.append((normalized_test_data[(i+1)*time_step:, :-1]).tolist())
    test_y.extend((normalized_test_data[(i+1)*time_step:, -1]).tolist())
    return mean, std, test_x, test_y

def try_model(time_step = 1):
    X = tf.placeholder(tf.float32, shape=[None, time_step, input_size])
    #mean,std,test_x,test_y=get_test_data([[20,2,0]],time_step,test_begin=0)
    normalized_data= (np.array([20,2,0])-sample_mean)/sample_std 
    x = [[normalized_data[:-1].tolist()]]
    y = [normalized_data[-1]]
    #print(x,y)
    with tf.variable_scope("sec_lstm",reuse=tf.AUTO_REUSE):
        pred,_=lstm(X)
    #saver=tf.train.Saver(tf.global_variables())
    # 读取图的信息
    saver = tf.train.import_meta_graph('./HelpPlay/models/tf_lstm/lstm02_BuzzLightyearPlanetRescue.meta')
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        #参数恢复
        module_file = tf.train.latest_checkpoint('./HelpPlay/models/tf_lstm/')
        saver.restore(sess, module_file)
        test_predict=[]
        prob=sess.run(pred,feed_dict={X:x})
        predict=prob.reshape((-1))
        # 还原等待时间预测值
        pre_wait_time = predict[0]*sample_std[-1]+sample_mean[-1]
        print(pre_wait_time)



if __name__ == "__main__":
    dataToTrain,dataToTest = read_csv()
    train_lstm(dataToTrain)
    prediction(dataToTest)
    test_prediction()
    #try_model()