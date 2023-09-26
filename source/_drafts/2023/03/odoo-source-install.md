---
title: 源代码方式安装 Odoo
date: 2022-12-08
updated: 2022-12-12
---

以 `ubuntu` 系统为例，参考：

<https://www.odoo.com/documentation/16.0/administration/install/install.html#postgresql>

## 源代码

```shell
git clone https://github.com/odoo/odoo.git
```

## 依赖检查

```shell
sudo apt install wkhtmltopdf
# wkhtmltopdf 版本要求： https://github.com/odoo/odoo/wiki/Wkhtmltopdf

# python>=3.7
sudo apt install python3-pip
python3 --version
pip3 --version

sed -n -e '/^Depends:/,/^Pre/ s/ python3-\(.*\),/python3-\1/p' debian/control | sudo xargs apt-get install -y

# 从右到左排版支持，先安装 nodejs 与 npm：https://github.com/nodesource/distributions/blob/master/README.md
sudo npm install -g rtlcss
```

## 数据库准备
```shell
sudo apt install postgresql postgresql-client
sudo su postgres
createuser -U postgres -P -s -e <db_user>
createdb -U <db_user> -h localhost <db_name>
```

## 运行

编辑配置文件 `vi ~/.odoorc`：
```shell
[options]
db_user=<db_user>
db_password=<db_password>
db_host=localhost
db_port=5432
database=<db_name>

addons_path=/path/to/odoo/addons

http_port=8080
```

运行：
```shell
python3 odoo-bin -d odoo -i base
```
