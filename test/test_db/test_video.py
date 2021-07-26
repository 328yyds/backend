from database.config import *
from database.table.video import *

data = session.query(Test_video).all()
print(data)