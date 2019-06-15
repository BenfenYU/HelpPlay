# 写代码的时候记下一些python的小东西

### 包的导入

##### 正规包
 当一个正规包被导入时，这个 __init__.py 文件会隐式地被执行，它所定义的对象会被绑定到该包命名空间中的名称。__init__.py 文件可以包
含与任何其他模块中所包含的 Python 代码相似的代码，Python 将在模块被导入时为其添加额外的属性。像这样的：
<pre>
    <span></span><span class="n">parent</span><span class="o">/</span>
    <span class="fm">__init__</span><span class="o">.</span><span class="n">py</span>
    <span class="n">one</span><span class="o">/</span>
        <span class="fm">__init__</span><span class="o">.</span><span class="n">py</span>
    <span class="n">two</span><span class="o">/</span>
        <span class="fm">__init__</span><span class="o">.</span><span class="n">py</span>
    <span class="n">three</span><span class="o">/</span>
        <span class="fm">__init__</span><span class="o">.</span><span class="n">py</span>
</pre>

    如果一个包里面的几个文件互相引用，那么不如放在同一个文件里面，或者设置一个子包，这样不至于很乱。