'''

    epoch，处理完所有数据并返回一次为一个epoch，1个epoch表示过了1遍训练集中的所有样本；batch-size：1次迭代所使用的样本量，由于数据量太大，
所以数据要分块的送进假设函数进行处理以及梯度下降，分成的块的一块就是一个batch；number of batch，是把所有数据分成了几个batch。
​    在TensorFlow的世界里，变量的定义和初始化是分开的，所有关于图变量的赋值和计算都要通过tf.Session的run来进行。想
要将所有图变量进行集体初始化时应该使用tf.global_variables_initializer。
​    Tensor-张量是基本的变量，然后进一步进行运算需要张量进化成图变量，然后初始化，然后在run()中进行计算。
    
    
    time step是时间步长，即用time_step个时间连续的数据来预测下一个时间的数据，其input格式是[batch_size, time_step, input_size]，input_size是时间维度，
自己现在的网络有偏差，所以决定先跑通，再仔细研究网络。'https://blog.csdn.net/frankiehello/article/details/79953482'可读。
也可以理解为展开的rnn或者lstm的block的个数。举个例子，如果是用rnn来做预测，输入1000条数据进行训练，
这1000条数据分为了10个batch，那么每个batch的batchsize就是100，然后我们如果是用前四个数值来预测第五个值的话，
输入的数据shape就是（100，4），这四个数值在时间上是连续的，所以图中的X0、X1、X2、X3就对应了这四个值，所以timestep就是4。


保存：saver.save(session, saved_path, global_step=None)
恢复：saver.restore(session, saved_path) 保存的文件有四种：
1. checkpoint，保存最近保存的模型的文件名，因此我们能够知道最近的模型名，可以通过调用tf.train.latest_checkpoint(dir)获知
2. .meta 图的结构，变量等信息
3. .data 参数值
4. .index 索引文件


不论batch或者time size是多少，训练输入和预测输入都要一样，如果预测时没有那么多值，就要用0补齐。
batch大一些可以提高计算效率，但是消耗也更大。

'''

'''
还未完成的：
1.模型的输入特征参数，需要更多，并且输入的值设置为多少比较合适
2.灵活的控制batch和time step。
'''

import numpy as np
import matplotlib.pyplot as plt
import os,math
import tensorflow as tf

csv_file_name = './HelpPlay/data/BuzzLightyearPlanetRescue.csv'
rnn_unit = 10  # 隐层数量
input_size =2 
output_size = 1
time_step = 1
lr = 0.0006  # 学习率
epochs = 500
originalData = []

sample_mean = np.array([70.76278837,  1.29588766]) 
sample_std = np.array([41.18567931 ,0.45644075])
y_mean = 17.899
y_std = 20.111

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
# 对数据做了标准化，公式是（原值-均值）/方差
# 并自己为数据分batch
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

# 用tf的api构建一个lstm网络模型
# 输入的参数X，不只是包含原始数据，还有batch和time step
# 必要时需要reshape得到用于训练的数据
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

# 理解初始化占位符时候的shape，有三个，分别指第一、二和三维有多少个元素，即a*b*c（三维的话一共是三层，即[[[*]]]）
# 占位符时在没有加入数据的时候使用的，用于抽象的配合网络，训练的时候用真实数据来feed占位符
# 模型的储存和读取在前面
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

# 自己写的利用模型来预测的函数，自行标准化，自行配置输入数据，自行跑一边模型的参数
def try_model(pre_data_list,time_step = 1):
    X = tf.placeholder(tf.float32, shape=[None, time_step, input_size])
    #mean,std,test_x,test_y=get_test_data([[20,2,0]],time_step,test_begin=0)
    normalized_data= (np.array(pre_data_list)-sample_mean)/sample_std 
    x = [[normalized_data.tolist()]]
    #y = [normalized_data[-1]]
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
        pre_wait_time = predict[0]*y_std+y_mean
        print(pre_wait_time)
    
    return pre_wait_time

#time = try_model([10,2])