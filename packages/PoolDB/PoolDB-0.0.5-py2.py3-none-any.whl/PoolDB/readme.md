## PoolDB 
#### python数据库连接池管理,支持并发获取sql数据，自动管理数据库连接，支持with语句，支持sql字典访问形式获取数据等

- 原生sql获取数据
```python
db_url = 'postgresql+psycopg2://xxx:xxx@xxx:5433/xxx?utf-8'
pool = PoolDB(db_url=db_url)
conn = pool.connect()
result = conn.execute(text("select * from xx.xx limit :limit"), limit=5)
while 1:
    try:
        r = next(result)
        print(r)
        print(r.xx)
    except:
        break
pool.close(conn)
```

- 并发获取数据库数据
```python
db_url = 'postgresql+psycopg2://xx:xx@xx:xx/xx?utf-8'
pool = PoolDB(db_url=db_url)
sqls = ["select * from xx.xx limit 5", "select * from xx.xx limit 4"]
gv = pool.multi_data(sql=sqls)  # 多条数据并发获取，
for v in gv:
    print(v)
```


- 字典形式访问获取数据库数据, key为sql或sql列表
```python
db_url = 'postgresql+psycopg2://xx:xx@xx:xx/xx?utf-8'
pool = PoolDB(db_url=db_url)
r = pool["select * from xxx.xxx limit 5"]  
print(r)
sqls = ["select * from xx.xx limit 5", "select * from xx.xx limit 4"]
r_list = pool[sqls]  
print(r_list)
```