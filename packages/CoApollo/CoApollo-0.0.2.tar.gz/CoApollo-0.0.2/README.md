# 文档转换器

cots.libs.apollo Apollo配置中心客户端,项目的目录结构如下。

## 目录结构

```
├── docs                        # 文档
├── apollo                      # 源码
├── tests                       # 测试示例文件
```

## 发布

```
# 生成依赖清单
pip freeze > requirements.txt

# 根据依赖清单安装环境
pip install -r requirements.txt


# 
python -m pip install setuptools wheel twine
pip install --user --upgrade setuptools wheel

# 本地安装
python setup.py install

# 构建输出
python setup.py sdist bdist_wheel

#上传包
twine upload --username Admin --password Admin --repository-url http://nuget.cityocean.com/pypi/COMS-Pypi/legacy dist/*

```
