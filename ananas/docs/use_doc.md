
## 三、使用

### 3.1 更改配置文件

根据具体需求更改ananas/config.py

### 3.2 自动生成错误码文档

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
### 3.3 自动生成文档更新日志文档

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
### 3.4 自动生成API接口文档

暂不支持

### 3.5 自动化部署

修改 make_docs.sh 文件

```
echo "开始部署..."
scp -r build/html/* root@192.168.10.154:/data/web/aoao/
echo "部署完毕."
```

### 3.6 生成文档

1. 更改配置文件
2. 将MarkDown文件放入/ananas/docs文件夹
3. 执行 sh make_docs.sh
4. 文档生成成功


