# 智慧树自动评论脚本

**背景**

+ 智慧树的某些课程评论互动分不根据参与讨论的绝对条数给分，而是根据所有学生参与的条数进行排名，根据排名的相对值赋分
+ 此行为加剧了内卷
+ 此行为导致评论区充斥着大量无意义问题，同时，回答也因复制粘贴而千篇一律

**解决方案**

+ 利用*科技手段*在我睡觉时帮我参与评论

## 一、功能与工具

**注意**：脚本采用 `Chrome Webdriver` 实现，严重依赖网页的元素布局。因此，该脚本**随时可能失效**

#### 1. 它可以做什么

+ 参与课程问答。依”最新“对问题排序，并选择回答数大于 10 的讨论参与回答
+ 对每一个回答的讨论，它会复制一条别人的回答，然后变成我的
+ 它将会把参与讨论的时间、题目、参与时已有的回答数和回答的内容记录在 `log.txt` 中

#### 2. 我需要准备什么

+ `Python 3`

+ `selenium` 库

  如果你没有，使用 `pip` 命令安装一下即可

+ `Chrome Webdriver`

  你可以在[这里](http://npm.taobao.org/mirrors/chromedriver/)很方便的下载与你的 Chrome 版本配套的 `Chrome Driver`

  至于如何使用它，你只需要下载好、解压、再把它放到 PATH 里即可

  > 如果你用的不是 `Chrome`
  >
  > 我们还支持 `FireFox`、`Edge` 和 `Safari`
  >
  > 你只需要下载对应的 WebDriver 并在代码里 `webdriver` 构造函数处做相应修改即可
  >
  > 具体可以百度你的浏览器的 `webdriver` 怎么安装
  >
  > 若要改动这部分内容，源程序涉及到两处改动
  >
  > 1. `getCookies.py` 第 21 行。例如，如果你使用的 `Edge`，修改为 `driver = webdriver.Edge()`
  > 2. `work.py` 第 44 行。修改同上

## 二、 开始使用

1. 准备好 `work.py` 和 `getCookies.py` 两个文件

2. 分别将两个文件头部的一些参数，依据注释进行修改

3. 在每次运行 `work.py` 前，需要先运行一次 `getCookies.py`，手动登录一次以获取 `Cookies`

   **注意**：运行此文件时，你只需输入账号密码回车登录即可，稍等片刻，程序会自动关闭浏览器

4. 运行 `work.py`

5. 去睡觉，睡醒检查你所设定的 `log` 文件