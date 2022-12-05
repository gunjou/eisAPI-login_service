from sqlalchemy import create_engine

SECRET_KEY = 'c06c5bbd202332b1ac34e7c0bd3ec660'

def get_connection():
    server = '192.168.0.250\ss2008r2'
    database = 'eis_jasamedika'
    username = 'sa'
    password = 'j4s4medik4'
    return create_engine(f'mssql+pymssql://{username}:{password}@{server}/{database}')
