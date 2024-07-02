
from flask_sqlalchemy import SQLAlchemy
import pymysql


db = SQLAlchemy()

pymysql.install_as_MySQLdb()

class Config:
    
    DEBUG = False

    
    
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/house'

    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
