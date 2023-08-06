

## Installation

install as **pip**

```shell
pip install nest-redis==1.1.0
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

  > :explain: 设置值
  >
  > :syntax: cache.set(key: str, val: object, [time: int,]) -> bool
  >
  > :param: key， 字符串的key
  >
  > :param: val， 字符串的值，可以为string,  list,  dict
  >
  > :param: time，超时时间，单位秒
  >
  > :return: string
  
  ```shell
  >>> cache.set("key", "val")
  >>> True
  >>> cache.set("key", "val", 3000)
  >>> True
  ```
  
- **get**

  >:explain: 获取值
  >
  >:syntax: cache.get(key: str) -> object
  >
  >:param: key，字符串的键
  >
  >:return: 字符串的值
  
  ```shell
  >>> cache.get("key")
  >>> "val"
  ```
  
- **ttl**

  > :explain: 获取该键剩余的时间
  >
  > :syntax: cache.ttl(key: str) -> int
  >
  > :param: key， 字符串的键
  >
  > :return: 剩余的时间，单位秒
  
  ```shell
  >>> cache.ttl("key")
  >>> 2990
  ```
  
- **persist**

  > :explain: 取消过期时间
  >
  > :syntax: cache.persist(key: str) -> bool
  >
  > :param: key，字符串的键
  >
  > :return: True设置成功，Flase设置失败
  
  ```shell
  >>> cache.persist(key)
  >>> True
  ```
  
- **expire**

  > :explain: 添加过期时间
  >
  > :syntax: cache.expire(key: str, time: int) -> bool
  >
  > :param: key， 字符串的键
  >
  > :param: time，过期的时间，单位秒
  >
  > :return: True设置成功，Flase设置失败
  
  ```shell
  >>> cache.expire(key, 2000)
  >>> True
  ```

#### 3. 队列相关方法

- **lpush**

  >:explain: 添加队首的值
  >
  >:syntax: cache.lpush(name: str, val: object) -> int
  >
  >:param: name，队列的键
  >
  >:param: val，队列的值
  >
  >:return: 返回队尾的值的索引

  ```shell
  >>> cache.lpush("colors", "red")
  >>> 1
  >>> cache.lpush("colors", ["yellow", "pink"])
  >>> 3
  ```

- **rpop**

  > :explain: 获取队尾的值
  >
  > :syntax: cache.rpop(name: str) -> object
  >
  > :param: name，队列的键
  >
  > :return: 返回队尾的值

  ```shell
  >>> cache.rpop("colors")
  >>> "red"
  ```

- **llen**

  > :explain: 获取队列的长度
  >
  > :syntax: cache.llen(name: str) -> int
  >
  > :param: name， 队列的key
  >
  > :return: 队列的长度
  
  ```shell
  >>> cache.llen("colors")
  >>> 2
  ```

#### 4. 哈希相关方法

- **hset**

  > :explain: 添加哈希数据
  >
  > :syntax: cache.hset(name: str, field: str, val: str) -> int
  >
  > :param: name，hash的键
  >
  > :param: field， hash的字段
  >
  > :param: val， hash的值
  >
  > :return:  0: 添加失败 1: 添加成功

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

  > :explain: 批量添加数据
  >
  > :syntax: cache.hmset(name :str, mapping: dict) -> bool
  >
  > :param: name，hash的名称
  >
  > :param: mapping，hash的数据，为字典类型
  >
  > :return: False: 添加失败 ; True: 添加成功

  ```shell
  >>> cache.hmset("company", {"mib": "{\"user_id\": 1207, \"user_name\":\"xxx\"}", "mic":"unknown"})
  >>> True
  ```

- **hgetall**

  > :explain: 获取hash中某个键下的键值对
  >
  > :syntax: cache.hgetall(name: str)-> dict
  >
  > :param: name，hash的名称
  >
  > :return: 哈希中name中的所有数据

  ```shell
  >>> cache.hgetall("shop")
  >>> {'3c': 'dell computer', 'food': 'egg', 'drink': 'milk'}
  ```

- **hget**

  > :explain: 获取哈希某字段下的数据
  >
  > :syntax: cache.hget(name: str, field: str) -> object
  >
  > :param: name，hash的名称
  >
  > :param: field，hash的字段名称
  >
  > :return: 哈希某字段下的数据(string, int, dict, list)

  ```shell
  >>> cache.hget("shop", "3c")
  >>> 'dell computer'
  ```

- **hlen**

  > :explain: 获取hash的长度
  >
  > :syntax: cache.hlen(name: str) -> int
  >
  > :param: name，hash的名称
  >
  > :return: hash的长度

  ```shell
  >>> cache.hlen("shop")
  >>> 3
  ```

- **hexists**

  > :explain: 判断一个field是否在hash中
  >
  > :syntax: cache.hexists(name: str, field: str) -> bool
  >
  > :param: name， hash的名称
  >
  > :param: field，   hash的字段名称
  >
  > :return: True: 存在  False:不存在
  
  ```shell
  >>> cache.hexists("shop", "3c")
  >>> True
  ```
  
- **hdel**

  > :explain: 删除hash中的字段信息
  >
  > :syntax: cache.hdel(name: str, field: str) -> int
  >
  > :param: name，hash的名称
  >
  > :param: field，hash的字段名称
  >
  > :return: 1:删除成功 0:删除失败
  
  ```shell
  >>> cache.hdel("shop", "3c")
  >>> 1
  ```

#### 5. 集合相关方法

- **sadd**

  > :explain: 添加集合数据
  >
  > :syntax: cache.sadd(name: str, val: object) -> int
  >
  > :param: name， 集合的键
  >
  > :param: val，  集合的值，可以为int or string
  >
  > :return: 1:成功 ； 0:失败

  ```shell
  >>> cache.sadd("names", "3c")
  >>> 1
  ```

- **smembers**

  > :explain: 获取集合中的数据
  >
  > :syntax: cache.smembers(name: str) -> set
  >
  > :param: name，集合的名称
  >
  > :return: 集合中的数据

  ```shell
  >>> cache.smembers("names")
  >>> {'3c'}
  ```

- **scard**

  > :explain: 获取集合的长度
  >
  > :syntax: cache.scard(name: str) -> int
  >
  > :param: name，集合的名称
  >
  > :return: 集合的长度

  ```shell
  >>> cache.scard("names")
  >>> 1
  ```

- **sismember**

  > :explain: 判断一个元素是否在集合中
  >
  > :syntax: cache.sismember(name: str, val: object) -> bool
  >
  > :param: name，集合的名称
  >
  > :param: val，需要查询的值
  >
  > :return: True在集合中，False不在集合中
  
  ```shell
  >>> cache.sismember("A", "v1")
  >>> True
  ```
  
- **sdiff**

  > :explain: 集合差集，属于A但不属于B
  >
  > :syntax: cache.sdiff(A: str, B: str) -> set
  >
  > :param: A， 集合A的键
  >
  > :param: B， 集合B的键
  >
  > :return: 集合差集
  
  ```shell
  >>> cache.sadd("A", ["v1", "v2", "v3"])
  >>> cache.sadd("B", "v2", "v4")
  >>> cache.sdiff("A", "B")
  >>> {"v1", "v3"}
  ```
  
- **sinter**

  > :explain: 集合交集，属于A且属于B
  >
  > :syntax: cache.sinter(A: str, B: str) -> set
  >
  > :param: A， 集合A的键
  >
  > :param: B， 集合B的键
  >
  > :return: 集合交集
  
  ```shell
  >>> cache.sadd("A", "v1", "v2", "v3")
  >>> cache.sadd("B", "v2", "v4")
  >>> cache.sinter("A", "B")
  >>> {"v2"}
  ```
  
- **sunion**

  > :explain: 集合并集，属于A或属于B的元素为称为A与B的并集
  >
  > :syntax: cache.sunion(A: str, B: str) -> set
  >
  > :param: A， 集合A的键
  >
  > :param: B，集合B的键
  >
  > :return: 集合并集
  
  ```shell
  >>> cache.sadd("A", "v1", "v2", "v3")
  >>> cache.sadd("B", "v2", "v4")
  >>> cache.sunion("A", "B")
  >>> {'v1', 'v2', 'v3', 'v4'}
  ```
  
- **srem**

  > :explain: 删除集合中的元素
  >
  > :syntax: cache.srem(name: str, *val: object) -> int
  >
  > :param: name，集合名称
  >
  > :param: val ，集合中的元素
  >
  > :return: 删除的个数

  ```shell
  >>> cache.srem("A", "a"， 2)
  >>> 2
  ```

#### 6. 有序集合相关方法

- **zadd**

  > :explain: 添加有序集合
  >
  > :syntax: cache.zadd(key: str, mapping: dict) -> list
  >
  > :param: key，有序集合的名称
  >
  > :param: mapping，要添加的值
  >
  > :return: 返回添加的个数
  
  ```shell
  >>> cache.zadd("A", {"a": 1, "b": 3, "c": 2})
  >>> 3
  ```
  
- **zrange**

  > :explain: 查询有序集合
  >
  > :syntax: cache.zrange(key: str, start: int, end: int) -> list
  >
  > :param: key，有序集合的名称
  >
  > :param: start，开始查询的索引
  >
  > :param: end，结束查询的索引
  >
  > :return:  获取查询后的元素的列表

  ```shell
  >>> cache.zrange("A", 0 , -1)
  >>> ['a', 'c', 'b']
  ```

- **zrank**

  > :explain: 查询有序集合的值的索引
  >
  > :syntax: cache.zrank(key: str, val: str) -> int
  >
  > :param: key，有序集合的名称
  >
  > :param: val， 需要查询的值
  >
  > :return: 返回查询该值的索引，索引为 -1 则表示不存在

  ```shell
  >>> cache.zrank("A", 'a')
  >>> 0
  ```
  
- **zcard**

  >:explain:  获取有序集合的长度
  >
  >:syntax: cache.zcard(key: str) -> int
  >
  >:param: key,  有序集合的名称
  >
  >:return: 有序集合的长度
  
  ```shell
  >>> cache.zcard("A")
  >>> 3
  ```
  
- **zscan_iter**

  > :explain:  有序集合的模糊匹配
  >
  > :syntax: cache.zscan_iter(name: str, match: str="*") -> list
  >
  > :param: name， 有序集合的名称
  >
  > :param: match， 匹配的字符串，默认为 *
  >
  > :return: 返回匹配的列表

  ```shell
  >>> cache.scan_iter("A"， "b*")
  >>> ['b', 'bf']
  ```

- **zrem**

  > :explain: 删除有序集合中的元素 
  >
  > :syntax: cache.zrem(name: str, *val: object) -> int
  >
  > :param: name，集合名称
  >
  > :param: val , 集合集合中的元素
  >
  > :return:  删除的个数

  ```shell
  >>> cache.zrem("A"， "a", "b")
  >>> 2
  ```

#### 7. 其他方法

- **delete**

  > :explain: 删除redis的键
  >
  > :syntax: cache.delete(key: str) -> int
  >
  > :param: key， redis的键
  >
  > :return:  1: 删除成功； 0：没有此key

  ```shell
  >>> cache.delete("A")
  >>> 1
  ```

- **flushdb**

  > :explain: 清除数据库下的所有键
  >
  > :syntax: cache.flushdb() -> bool
  >
  > :return: True清空成功，False清空失败
  
  ```shell
  >>> cache.flushdb()
  >>> True
  ```
  
- **handler**

  > :explain: 获取redis句柄
  >
  > :syntax: cache.handler() -> object
  >
  > :return: object
  
  ```shell
  >>> handler = cache.handler()
  >>> handler.get("a")
  >>> "12345"
  ```