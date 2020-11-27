把特定文章所使用的图片放在特定文件夹中可以便于更好的管理，顺便熟悉Python的相关操作



可以移动以下格式的图片

``` 
![test.png](../posts/test.png) -> ![test.png](../posts/{title}/test.png)
![test.png](test.png) ->  ![test.png](../posts/{title}/test.png)
```

由于对于正则表达式还不够熟练，所以对于开头的空格`/space /![test.png](test.png)`实在不知道该如何匹配，但是只有少量，所以手动修改了。

sm.ms爬不了。。所以也是自己动手丰衣足食



