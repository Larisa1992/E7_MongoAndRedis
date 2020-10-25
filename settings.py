# Замените user, password, example.com, database на ваши данные доступа к БД.
# MONGO_URI = "mongodb://user:password@example.com:27017/database"

# mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'board'


DATE_FORMAT = '%Y-%m-%d'

# допустимые методы для пути
# /document/
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# допустимые методы для пути
# /document/<ObjectId>
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

    # Описываем ресурс `/document`
document = {
           
    # 'url': 'doc/id/<regex("[a-f0-9]{24}"):document_id>',

    'schema': {
        'title': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 100,
        },
        'date': {
            'type': 'datetime',
        },
        'message': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 250,
        },
        'author': {                
            'type': 'string',
        },
        'images': {
            'type': 'list', # тип: список
        },
        'tags': {
            'type': 'list',
        },
        'comments': {
            'type': 'list',
        }
    }
}

DOMAIN = {'document': document,}