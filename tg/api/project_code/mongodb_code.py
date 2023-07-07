import pymongo

# 连本机mongodb（参数可不写）
# client = MongoClient(host='localhost', port=27017)

'''
mongodb数据库配置
'''
class MongodbSql:
    def __init__(self):
        self.__url = 'mongodb+srv://tushanjiexian:qq2764098241@cluster0.kxbpcwo.mongodb.net/?retryWrites=true&w=majority'

    # 新建连接
    def connect(self, database, gather):
        client = pymongo.MongoClient(self.__url, maxPoolSize=300)  # 建立连接，maxPoolSize连接池最大值，默认100
        if database in client.list_database_names():
            print("数据库已存在！")

        db = client[database]  # 进入数据库
        if gather in db.list_collection_names():
            print("集合已存在！")

        collection = db[gather]
        return collection

    # 修改连接链接
    def set_url(self, url):
        self.__url = url

    # 读取连接链接
    @property
    def get_url(self):
        return self.__url


'''
mongodb数据库集合操作
'''
class MongoOperation:
    def __init__(self, collection):
        self.collection = collection

    def __for_data(self, values, kwargs_items):
        for j, k in kwargs_items.items():
            values[j] = k
        return values

    # 新增一条数据
    def insert_one(self, user, data, **kwargs):
        data_insert = {"user": user, "data": data}
        data_insert = self.__for_data(data_insert, kwargs)
        return self.collection.insert_one(data_insert)

    # 批量新增数据
    def insert_all(self, data_all):
        # for data in data_all:
        #     self.insert_one(**data)
        return self.collection.insert_many(data_all)

    # 查询指定数据
    def get_one(self, user, **kwargs):
        data_query = {'user': user}
        data_query = self.__for_data(data_query, kwargs)
        t = list(self.collection.find(data_query, {"_id": 0}))
        return {} if len(t) == 0 else t[0]

    # 查询所有数据
    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))

    # 修改一条目标数据
    def update_one(self, user, data, **kwargs):
        old_query = {"user": user}
        values = {'data': data}
        values = self.__for_data(values, kwargs)
        new_values = {"$set": values}

        return self.collection.update_one(old_query, new_values)

    # 修改所有目标数据
    def update_all(self, user, data, **kwargs):
        old_query = {"user": user}
        values = {'data': data}
        values = self.__for_data(values, kwargs)
        new_values = {"$set": values}
        return self.collection.update_many(old_query, new_values)

    # 删除一条目标数据
    def delete_one(self, user, **kwargs):
        data_query = {"user": user}
        data_query = self.__for_data(data_query, kwargs)
        self.collection.delete_one(data_query)

    # 删除所有目标数据
    def delete_all(self, user, **kwargs):
        data_query = {"user": user}
        data_query = self.__for_data(data_query, kwargs)
        return self.collection.delete_many(data_query)

    # 删除所有数据
    def delete_many(self):
        return self.collection.delete_many({})

    # 删除当前集合
    def delete_drop(self):
        self.collection.drop()


'''
控制器
'''
class Controller:
    def __init__(self, database, gather):
        self.mongodbSql = MongodbSql()
        self.collection = self.mongodbSql.connect(database, gather)
        self.musicFlakeVue = MongoOperation(self.collection)


if __name__ == '__main__':
    mongodbSql = MongodbSql()
    collection = mongodbSql.connect('mongoFlaskVue', 'userInfo')
    musicFlakeVue = MongoOperation(collection)

    musicFlakeVue.delete_many()

    musicFlakeVue.insert_one('liulijiexian', [])
    print(list(musicFlakeVue.get_all()))

    musicFlakeVue.update_one('liulijiexian', [{'a': 1}])
    print(musicFlakeVue.get_one('liulijiexian'))

    musicFlakeVue.delete_one('liulijiexian')
    print(list(musicFlakeVue.get_all()))
    print(list(musicFlakeVue.get_one('liulijiexian')))
