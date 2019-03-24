# 数据拟合

​	2019-02-18 划分时间段进行训练，抽掉不重要的数据，时间用自然序号代替，每天循环。为训练的网络增加输入参数，比如特殊的节假日，雨雪天气，等等。输入的参数能否包括前一时间点的等待时间？毕竟有点马尔科夫链的感觉。
​    编程后期一定要加入日志，关键位置一定要记录下来，方便以后调试。

# 机器学习


​	epoch，处理完所有数据并返回一次为一个epoch；batch，由于数据量太大，所以数据要分块的送进假设函数进行处理以及梯度下降，分成的块的一块就是一个batch；number of batch，是把所有数据分成了几个batch。
​    在TensorFlow的世界里，变量的定义和初始化是分开的，所有关于图变量的赋值和计算都要通过tf.Session的run来进行。想
要将所有图变量进行集体初始化时应该使用tf.global_variables_initializer。
​    Tensor-张量是基本的变量，然后进一步进行运算需要张量进化成图变量，然后初始化，然后在run()中进行计算。

# python
​	处理线程的时候遇到，在传参为函数名字的时候，会在调用的位置执行该传入的函数；在传参为函数名加括号的时候，会优先执行该传参的函数，真坑。

# lstm
    由于几个输入的维度之间最好步要有相关性，那就只要输入前五分钟的数据好了，再有就是旅游舒适度、节假日和日期的序列。

    influx  -database 'disney' -host 'localhost' -execute 'SELECT * FROM "disney"' -format 'csv' > 0324.csv
    
保存：saver.save(session, saved_path, global_step=None)
恢复：saver.restore(session, saved_path) 保存的文件有四种：
1. checkpoint，保存最近保存的模型的文件名，因此我们能够知道最近的模型名，可以通过调用tf.train.latest_checkpoint(dir)获知
2. .meta 图的结构，变量等信息
3. .data 参数值
4. .index 索引文件

    time step指的是，文本处理中，一个单词代表一个timestep，在inference的时候，只能一个单词一个单词地输出；而在train的时候，我们有整个句子，因此可以一次feed若干个单词，比如Google is better than Apple，timestep为5，同时训练目标为is better than Apple [END]。

    不论batch或者time size是多少，训练输入和预测输入都要一样，如果预测时没有那么多值，就要用0补齐。
    batch大一些可以提高计算效率，但是消耗也更大。