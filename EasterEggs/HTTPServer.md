# HTTPServer

如果想让身边的朋友或同事临时访问你电脑中的某个文件目录，通常的做法是搭一个共享目录出来供大家访问。

不过你要是安装了Python，那么一切都变得简单很多了，只需要打开命令行窗口，切换到指定目录，执行：

> python -m SimpleHTTPServer  # python2

> python -m http.server  # python3

这是 Python 内置的一个简单 HTTP Server，方便自己、他人用浏览器来访问文件目录