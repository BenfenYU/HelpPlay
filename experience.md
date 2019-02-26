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