import kafkaModule
from datetime import datetime

create_topic = "AIServiceEnabler_requestData"
create_topic2 = "AIServiceEnabler_responseData"
create_data = {"id":"yujin","createDate":datetime.today().strftime("%Y/%m/%d %H:%M:%S")}

kafkaModule.Producer(create_topic, create_data)
kafkaModule.Producer(create_topic2, create_data)