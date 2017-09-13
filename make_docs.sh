#!/bin/bash
echo "Api文档生成小工具v1.0"
vim template/_version/note
vim template/_version/version
echo "开始生成文档...."
python ananas/set_error.py
python ananas/set_log.py set_markdown
python ananas/set_log.py initialize
python ananas/set_index.py
make html
echo "文档生成完毕."

#echo "开始部署..."
#scp -r build/html/* root@192.168.10.154:/data/web/aoao/
#echo "部署完毕"



