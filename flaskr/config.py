# musqlの時は、hogehogeの所に実際のdb名を入力する
# pip install PyMySQL もやるように
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/hogehoge?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr.db'
SECRET_KEY = 'secret key'
JSON_AS_ASCII = False
JSON_SORT_KEYS = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
