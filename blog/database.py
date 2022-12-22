from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog/blog.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, conect_args={'check_same_thread': False}, echo=True)
