import redis

from bson.objectid import ObjectId
from eve.io.mongo import mongo
from eve import Eve

r = redis.StrictRedis(host='localhost', port=6379, db=0)

app = Eve(settings='settings.py', redis=r)
mongo = app.data.driver

def after_fetching_document(response):
    list_id = response['_id']
    f = {'list_id': ObjectId(list_id)}
    rr = response['items'] 
    print(f'response items = {rr}')
    print(f'list = {list(mongo.db.items.find(f))}')

# def before_returning_items(resource_name, response):
#     print('About to return items from "%s" ' % resource_name)
#     print('About to return items from "%s" ' % response)
#     return resource_name

# def before_returning_item(resource_name, response):
#     print('About to return an item from "%s" ' % resource_name)
#     return resource_name

def pre_document_get_callback(request, lookup):   
    print(f'lookup {lookup} request {request.args} {type(request)}')
    print('A GET request on the document endpoint has just been received!')
    return lookup


def before_returning_document(response):
    f = request.get_json()
    print(f)
    print('About to return a contact')

# добавляем к ответу GET запроса вычисляемые значения
def calc_counts(endpoint, response):
    for document in response['_items']:
        # считаем количество тэгов
        try:
            count_tag = len(document['tags'])
            document['count_tag'] = count_tag
        except KeyError:
            pass
        # считаем количество комментариев
        try:
            count_comments = len(document['comments'])
            document['count_comments'] = count_comments
        except KeyError:
            pass

# @app.route('/document/<regex("[a-f0-9]{24}"):document_id>/tag', methods=['POST'])
@app.route('/document/<string:tag>/<regex("[a-f0-9]{24}"):document_id>', methods=['POST'])
def add_tag_2(tag, document_id):
    print(tag)
    print(f'app route document tag {document_id}')
    
    f = {'_id': ObjectId(document_id)}
    # f = {"_id": document_id}
    # dd = mongo.db.document.find_one({'_id': ObjectId('5f91ed9b8feeb0154df74c4e')})
    dd = mongo.db.document.find_one(f)
    
    # {"$addToSet": {"tags": dict(data)}}
    # mongo.db.document.update_one(f, {'$set':{"message": "update message from request"}})
    mongo.db.document.update_one(f, {'$addToSet':{"tags": tag}})
    # print(f, type(dd), dd['message'])

    # dd_all = mongo.d
    # b.document.find()
    # for d in dd_all:
#     #     print(d, type(d))
#     # print(f, type(dd))
    return f'hello world! I have add tag to document {document_id}'

@app.route('/comment/<string:comment>/<regex("[a-f0-9]{24}"):document_id>', methods=['POST'])
def add_comment(comment, document_id):
    print(comment)
    print(f'app route document comment {document_id}')
    f = {'_id': ObjectId(document_id)}
    dd = mongo.db.document.find_one(f)
    
    # {"$addToSet": {"tags": dict(data)}}
    # mongo.db.document.update_one(f, {'$set':{"message": "update message from request"}})
    mongo.db.document.update_one(f, {'$set':{"comments": comment}})
    # print(f, type(dd), dd['message'])
    return f'I have add comment to document {document_id}'

# /documents POST
def add_tag(response):
    document_id = None
    print(response[0]['_id'])
    try:
        document_id = response[0]['_id']
    except KeyError:
        pass
    if (document_id is not None): 
        print(document_id)
        print(type(response[0]['tags']))

    print(f'add tags {response}')

# кэшируем создание поста
def for_cache(response):
    print(response[0]['_id'])
    r.set(str(response[0]['_id']), ';'.join(str(atr) for atr in response))
    print('will bi cache')

# def add_comment(resoutce, items):

# attach a callback function to POST requests.
app.on_inserted_document += for_cache

#  not work
app.on_fetched_document += for_cache
# перехват отрисовки ответа
app.on_fetched_resource += calc_counts

# app.on_fetched_item_document += after_fetching_document

app.on_pre_GET_document += pre_document_get_callback
app.on_fetched_item_document += before_returning_document

# app.on_fetched_item_document += add_tag_2
# app.on_fetched_item_document += add_tag

# app.on_fetched_resource += before_returning_items

# app.on_fetched_item += before_returning_item

# @app.route('/document/<regex("[a-f0-9]{24}"):document_id>/tag')
# def hello_world(document_id):
#     return f'hello world! I have add tag to document {document_id}'

if __name__ == '__main__':
    app.run()