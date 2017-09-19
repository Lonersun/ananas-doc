# ananas-doc

ananas-doc 是基于sphinx封装的用于生成文档的小工具，它具有一下特点：

* 解决了Sphinx只支持reStructuredText语法的问题，它可以完美的支持MarkDown语法，不用再二次转换成.rst文件
* 引入了sphinx_rtd_theme主题，并在此基础上进行了优化，使界面更加美观；
* 增加了文档更新日志的功能，使每次升级都有记录；
* 增加了错误码生成功能，可自动生成错误码；
* 增加自定义配色方案，界面调整更加简单，
* 配合yml接口定义自动生成接口文档，减轻了文档维护的成本

## 安装

python == 2.7

安装方法：

```
pip install ananas-doc

```


## 使用

### 初始化

```
ananas-mkdoc <project name>

```

### 更改配置文件

根据具体需求更改conf.py

### 自动生成错误码文档

```
# 错误码文档生成配置
errors_doc_config = {
    # 是否要生成错误码文档
    "if_set_errors": True,

    # 错误码所在模块路径
    "module_dir": "/path",

    # 错误码所在模块名称
    "module_name": "errors",

    # 错误码文档生成标题
    "error_title": "三、错误对照表",
}
```
### 自动生成文档更新日志文档

```
# 文档更新日志
log_doc_config = {
    # 是否要生成日志
    "if_set_log": True,

    # 更新作者
    "author": "Lonersun",

    # 日志标题
    "log_title": "四、更新日志",
}
```

### 自动生成API接口文档

暂不支持

### 添加需要更改的MarkDown文件

```
index_doc_config = {

    # 文档标题
    'title': "Ananas",

    # 文档简介
    'content': "Ananas",

    # 需要包含的MarkDown文件 如开启了错误码、日志自动生成，请添加 docs/log.md  docs/error.md
    "nav": []
}

```

### 自定义页面效果

请修改 template/_static

### 自定义Logo

请替换 template/_static/images/logo.png

### 生成文档

1. 更改配置文件
2. 将MarkDown文件放入docs文件夹
3. 执行 make doc
4. 文档生成成功


示例Demo: 
[http://docs.lonersun.com](http://docs.lonersun.com)


