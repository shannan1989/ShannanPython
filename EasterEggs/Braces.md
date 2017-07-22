# 大括号替换缩进

Python的目标之一就是让程序员少打些字，让生活多些乐趣。

Python不需要像类C语言一样输入 begin/end、then/endif 或者 {} 来结束代码块，Python使用缩进来结束代码块。

而braces库算得上是Python中最恶搞的一个彩蛋了。

如果你是从类C语言转过来的程序员，估计你是一时半会儿适应不了Python的缩进，那么是否有其他办法呢？

braces模块就是专门为C程序员准备的兼容方案。

> from \_\_future__ import braces

> File "\<stdin>", line 1  
SyntaxError: not a chance
  
哈哈，被骗了吧，窃以为导入braces就可以使用大括号来结束代码块，Python告诉你的答案是：没门儿！