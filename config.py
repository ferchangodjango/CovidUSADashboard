
class SecretKey():
    SECRET_KEY='JOKEER89$'

class AppConfig(SecretKey):
    DEBUG=True
    MYSQL_HOST='localhost'
    MYSQL_PORT=3306
    MYSQL_USER='root'
    MYSQL_PASSWORD='89JQuery78#'
    MYSQL_DB='ecomers'

externalObject={
    'config':AppConfig()
}
    