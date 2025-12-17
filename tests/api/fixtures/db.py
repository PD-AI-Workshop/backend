# import pytest

# from db.session import async_engine


# # @pytest.fixture(autouse=True, scope='function')
# # def db_cleanup():
# #     connection = async_engine.connect()
# #     transaction = connection.begin()
    
# #     yield
    
# #     transaction.rollback()
# #     connection.close()