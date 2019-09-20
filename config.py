import os


class Config:
    # tell flask location of database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://postgres:gian@localhost/mkoani'
    SQL_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mbazi is bananas'
    MAIL_SERVER = ''  # example smtp.gmail.com
    MAIL_PORT = 25  # example 25
    MAIL_USERNAME = ''  # example anotherone@gmail.com
    MAIL_PASSWORD = ''  # google account password is using gmail (Not recommended)
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'register@mkoani.com'  # example google email if using gmail
    #
    #
