# ADT

## vector

特点：静态的，区间一开始就是划分好的，在物理上是连续的存储空间，可以根据秩直接确定物理位置

定义：数组的抽象与泛化，是一种线性序列

构造函数/实现：new一个数组，或是用copyfrom复制已有的数组 | vector

保护接口：

- copyfrom：复制 - new一个二倍size的数组[避免后期不必要的扩容]，后循环填入
- expend：扩容 - 成倍的扩充capacity，循环填入，使用加倍的方式扩容的时间成本更低，递增式空间成本低
- shrink：缩容 - 当填装因子小于1/4，成倍的缩小capacity

对外接口：

- size
- insert
- put
- find
- search
- sort
- disordered
- []
- remove
- delete
- duplicate
- uniquify

## List

定义：以节点作为基本元素，使用前驱和后继来实现逻辑上的线性序列。

特点：可以双向访问

初始化：双向链表，定义头尾俩哨兵以及size为0

接口：与vector差不多，但是实现有区别

## Stack

定义：只能通过top端进行访问

特点：LIFO

实现：继承vector

接口：

- push
- top
- empty
- size
- pop

应用场景：

1. 逆序输出：短除法进制转换
2. 递归嵌套：括号匹配
3. 延迟缓冲：中缀表达式[常用的] - 算术表达式求值 - 数栈+符号栈
4. 栈式计算：RPN逆波兰表达式计算[后缀] - 算术表达式求值 - 遇到符号从栈中取数计算

数学计算：

1. [栈混洗问题](https://next.xuetangx.com/learn/THU08091000384/THU08091000384/4215507/video/6083694
   )，栈种类的数目，结果为卡塔兰数，(2n!)/((n+1)!*n!)

## queue

定义：尾部插入，头部输出的线性序列

实现：继承list，额外实现enqueue，dequeue等

特点：FIFO

接口：

- rear
- front
- enqueue
- dequeue
- empty
- size

## 树

定义：以层次结构来组织数据项

特点：非线性结构，但具有线性结构的特征，同时集合vector的search快，以及list的remove和insert快的优点。连通性，无环性

有序树：兄弟之间有编号，可以表现优先级

边的数量：等于节点数-1，或者是度数

路径长度：可用边的数量/点的数量，用边更方便

高度：空树高度为-1

序列表示法：父节点表示法、孩子节点表示法、父亲孩子表现法、长子兄弟表示法

接口：

- root
- parent
- firstchild
- nextsibling
- insert
- remover
- traverse

## 二叉树

定义：只有迪两个孩子

特点：可表示任何树，是基于长子兄弟表示法衍生的，涨宽速度更快

深度：logn向上取整

数量：每层最大数目是2的深度次方，点的数量最大为底层的两倍

节点模板类：BinNode - 带有一些额外的指标

节点的接口：

- insertAsLC
- insertAsRC
- succ
- travLevel
- travPre
- travIn
- travPost

BinTree接口：

protected：

- updateHeight
- updateHeightAbove

public:

- size
- empty
- root

树的重构：中序 + 【前序 | 后序】或者 真二叉 + 前序 + 后序

## Graph

定义：一堆边以及节点的集合

类别：有向图、无向图、有环图、无环图

欧拉环路：覆盖所有有向边且恰好一次的环路

哈密尔顿环路：每个节点只经过一次的简单环路

简单：不重复

实现：邻接矩阵、关联矩阵

点的结构：数据、发现/访问时间、父亲、状态、优先级、构造函数

边的结构：数据、权重、类型，构造函数

邻接矩阵评价：实现简单、运用广泛、使用效率高、良好的扩展性，空间性能不得行





