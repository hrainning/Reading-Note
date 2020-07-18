# ADT

## vector

定义：数组的抽象与泛化，是一种线性序列

构造函数：new一个数组，或是用copyfrom复制已有的数组 | vector

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