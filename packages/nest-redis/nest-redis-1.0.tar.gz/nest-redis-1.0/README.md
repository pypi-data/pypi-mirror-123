

## Installation

install as **pip**

```shell
pip install nest-redis==1.0
```

## Usage

#### 1. 实例化

- redis配置

  ```python
  config = {
      "host": "127.0.0.1",
      "port": 6379,
      "password": "123456",
      "db": 61,
      "decode_responses": True
  }
  ```

- 获取句柄

  ```python
  >>> from pyredis.cache import RedisUtil
  >>> cache = RedisUtil(config)
  ```


#### 2.字符串相关方法

- **set**

  > 功能: 设置值
  >
  > 语法: `cache.set(key: str, val: object, [time: int,]) -> bool`
  >
  > key : 字符串的key
  >
  > val : 字符串的值，可以为string,  list,  dict
  >
  > time: 超时时间

  ```shell
  >>> cache.set("key", "val")
  >>> True
  >>> cache.set("key", "val", 3000)
  >>> True
  ```
  
- **get**

  >功能: 获取值
  >
  >语法: `cache.get(key: str) -> object`
  >
  >key: 字符串的key

  ```shell
  >>> cache.get("key")
  >>> "val"
  ```
  
- **ttl**

  > 功能: 取消过期时间
  >
  > 语法: `cache.ttl(key: str) -> int`
  >
  > key: 字符串的key

  ```shell
  >>> cache.ttl("key")
  >>> 2990
  ```
  
- **persist**

  > 功能: 取消过期时间
  >
  > 语法: `cache.persist(key: str) -> bool`
  >
  > key: 字符串的key

  ```shell
  >>> cache.persist(key)
  >>> True
  ```
  
- **expire**

  > 功能: 添加过期时间
  >
  > 语法: `cache.expire(key: str, time: int) -> bool`
  >
  > key: 字符串的key
  >
  > time: 过期的时间，单位秒

  ```shell
  >>> cache.expire(key, 2000)
  >>> True
  ```

#### 3. 队列相关方法

- **lpush**

  >功能: 添加队首的值
  >
  >语法: `cache.lpush(key: str, val: object) -> int`
  >
  >key: 队列的key
  >
  >val: 队列的值，可以为string, int, list
  >
  >return: int 返回队尾的值的索引

  ```shell
  >>> cache.lpush("colors", "red")
  >>> 1
  >>> cache.lpush("colors", ["yellow", "pink"])
  >>> 3
  ```

- **rpop**

  > 功能: 获取队尾的值
  >
  > 语法: `cache.rpop(key: str) -> object`
  >
  > key: 队列的key
  >
  > return: obejct 返回队尾的值

  ```shell
  >>> cache.rpop("colors")
  >>> "red"
  ```

- **llen**

  > 功能: 获取队列的长度
  >
  > 语法: `cache.llen(key: str) -> int`
  >
  > key: 队列的key
  >
  > return: 队列的长度
  
  ```shell
  >>> cache.llen("colors")
  >>> 2
  ```

#### 4. 哈希相关方法

- **hset**

  > 功能: 添加哈希数据
  >
  > 语法: `cache.hset(name: str, field: str, val: str) -> int`
  >
  > name: hash的key
  >
  > field: hash的字段名
  >
  > val: hash的值，字符串类型
  >
  > return : 0: 添加失败 1: 添加成功

  ```shell
  >>> cache.hset("shop", "3c", "dell computer")
  >>> 1
  >>> cache.hset("shop", "drink", "milk")
  >>> 1
  >>> cache.hset("shop", "food", "egg")
  >>> 1
  >>> cache.hset("shop", "cigarette", {"liqun":17, "huangjinye": 12})
  >>> 1
  ```

- **hmset**

  > 功能: 批量添加数据
  >
  > 语法: `cache.hmset(name :str, mapping: dict) -> bool`
  >
  > name: hash的名称
  >
  > mapping:  hash的数据，为字典类型
  >
  > return : False: 添加失败 ; True: 添加成功

  ```shell
  >>> cache.hmset("company", {"mib": "{\"user_id\": 1207, \"user_name\":\"xxx\"}", "mic":"unknown"})
  >>> True
  ```

- **hgetall**

  > 功能: 添加过期时间
  >
  > 语法: `cache.hgetall(name: str)-> dict`
  >
  > name: hash的名称
  >
  > return 哈希中name中的所有数据

  ```shell
  >>> cache.hgetall("shop")
  >>> {'3c': 'dell computer', 'food': 'egg', 'drink': 'milk'}
  ```

- **hget**

  > 功能: 获取指定的数据
  >
  > 语法: `cache.hget(name: str, field: str) -> object`
  >
  > key: hash的名称
  >
  > field: hash的字段名称
  >
  > 返回值：string or dict or list

  ```shell
  >>> cache.hget("shop", "3c")
  >>> 'dell computer'
  ```

- **hlen**

  > 功能: 获取hash的长度
  >
  > 语法: ` cache.hlen(name: str) -> int `
  >
  > name: 字符串的名称
  >
  > return : hash的长度

  ```shell
  >>> cache.hlen("shop")
  >>> 3
  ```

- **hexists**

  > 功能: 判断一个field是否在hash中
  >
  > 语法: `cache.hexists(name: str, field: str) -> bool`
  >
  > name: hash的名称
  >
  > field: hash的字段名称
  >
  > return: True: 存在  False:不存在
  
  ```shell
  >>> cache.hexists("shop", "3c")
  >>> True
  ```
  
- **hdel**

  > 功能: 删除hash中的字段信息
  >
  > 语法: `cache.hdel(name: str, field: str) -> int`
  >
  > name: hash的名称
  >
  > field: hash的字段名称
  >
  > return: 1:删除成功 0:删除失败
  
  ```shell
  >>> cache.hdel("shop", "3c")
  >>> 1
  ```

#### 5. 集合相关方法

- **sadd**

  > 功能: 添加集合数据
  >
  > 语法: `cache.sadd(key: str, val: object) -> int `
  >
  > key: 集合的key
  >
  > val:  集合的值，可以为int or string
  >
  > return: 1:成功 ； 0:失败

  ```shell
  >>> cache.sadd("names", "3c")
  >>> 1
  ```

- **smembers**

  > 功能: 获取集合中的数据
  >
  > 语法: `cache.smembers(key) -> set `
  >
  > key: 集合的名称
  >
  > return: 集合中的数据

  ```shell
  >>> cache.smembers("names")
  >>> {'3c'}
  ```

- **scard**

  > 功能: 获取集合的长度
  >
  > 语法: `cache.scard(key: str) -> int`
  >
  > key: 集合的名称

  ```shell
  >>> cache.scard("names")
  >>> 1
  ```

- **sismember**

  > 功能: 判断一个元素是否在集合中
  >
  > 语法: `cache.sismember(name: str, val: object) -> bool`
  >
  > name: string, 集合的名称
  >
  > val: 需要查询的值

  ```shell
  >>> cache.sismember("A", "v1")
  >>> True
  ```
  
- **sdiff**

  > 功能: 集合差集，属于A但不属于B
  >
  > 语法: `cache.sdiff(A: str, B: str) -> set`
  >
  > A:  集合A
  >
  > B:  集合B

  ```shell
  >>> cache.sadd("A", ["v1", "v2", "v3"])
  >>> cache.sadd("B", "v2", "v4")
  >>> cache.sdiff("A", "B")
  >>> {"v1", "v3"}
  ```
  
- **sinter**

  > 功能: 集合交集，属于A且属于B
  >
  > 语法: `cache.sinter(A: str, B: str) -> set `
  >
  > A:  集合A
  >
  > B:  集合B

  ```shell
  >>> cache.sadd("A", "v1", "v2", "v3")
  >>> cache.sadd("B", "v2", "v4")
  >>> cache.sinter("A", "B")
  >>> {"v2"}
  ```
  
- **sunion**

  > 功能: 集合并集，属于A或属于B的元素为称为A与B的并集
  >
  > 语法: `cache.sunion(A: str, B: str) -> set `
  >
  > A:  集合A
  >
  > B:  集合B

  ```shell
  >>> cache.sadd("A", "v1", "v2", "v3")
  >>> cache.sadd("B", "v2", "v4")
  >>> cache.sunion("A", "B")
  >>> {'v1', 'v2', 'v3', 'v4'}
  ```
  
- **srem**

  > 功能: 删除集合中的元素
  >
  > 语法: `cache.srem(name: str, *val: object) -> int `
  >
  > name: 集合名称
  >
  > val ： 集合中的元素
  >
  > return :  删除的个数

  ```shell
  >>> cache.srem("A", "a"， 2)
  >>> 2
  ```

#### 6. 有序集合相关方法

- **zadd**

  > 功能: 添加有序集合
  >
  > 语法: `cache.zadd(key: str, mapping: dict) -> list`
  >
  > key: 有序集合的名称
  >
  > mapping: 有序集合的值,类型为dict

  ```shell
  >>> cache.zadd("A", {"a": 1, "b": 3, "c": 2})
  >>> 3
  ```
  
- **zrange**

  > 功能: 查询有序集合
  >
  > 语法: `cache.zrange(key: str, start: int, end: int) -> list`
  >
  > key: 有序集合的名称
  >
  > start: 开始查询的索引
  >
  > end: 结束查询的索引

  ```shell
  >>> cache.zrange("A", 0 , -1)
  >>> ['a', 'c', 'b']
  ```

- **zrank**

  > 功能: 查询有序集合的值的索引
  >
  > 语法: `cache.zrank(key: str, val: str) -> int`
  >
  > key: 有序集合的名称
  >
  > val: 需要查询的值
  >
  > return: 返回查询该值的索引，索引为 -1 则表示不存在

  ```shell
  >>> cache.zrank("A", 'a')
  >>> 0
  ```
  
- **zcard**

  >功能:  获取有序集合的长度
  >
  >语法: `cache.zcard(key: str) -> int`
  >
  >key: 有序集合的名称

  ```shell
  >>> cache.zcard("A")
  >>> 3
  ```
  
- **zscan_iter**

  > 功能:  有序集合的模糊匹配
  >
  > 语法: `cache.zscan_iter(name: str, match: str="*") -> list`
  >
  > name: 有序集合的名称
  >
  > match: string, 匹配的字符串，默认为 *
  >
  > return: 返回匹配的列表

  ```shell
  >>> cache.scan_iter("A"， "b*")
  >>> ['b', 'bf']
  ```

- **zrem**

  > 功能: 删除有序集合中的元素
  >
  > 语法: `cache.zrem(name: str, *val: object) -> int `
  >
  > name: 集合名称
  >
  > val ： 集合中的元素
  >
  > return :  删除的个数

  ```shell
  >>> cache.zrem("A"， "a", "b")
  >>> 2
  ```

#### 7. 其他方法

- **delete**

  > 功能: 删除redis的键
  >
  > 语法: `cache.delete(key: str) -> int`
  >
  > key: redis的键
  >
  > return: 1: 删除成功； 0：没有此key

  ```shell
  >>> cache.delete("A")
  >>> 1
  ```

- **flushdb**

  > 功能: 清除数据库下的所有键
  >
  > 语法: `cache.flushdb() -> bool `

  ```shell
  >>> cache.flushdb()
  >>> True
  ```
  
- **handler**

  > 功能: 获取redis句柄
  >
  > 语法: `cache.handler()`

  ```shell
  >>> handler = cache.handler()
  >>> handler.get("a")
  >>> "12345"
  ```
  