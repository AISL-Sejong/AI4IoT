import kafkaModule

create_topic = "AIServiceHub_requestData"
create_topic2 = "AIServiceHub_responseData"
create_data = {"id":"user","createDate":"20XX.XX.XX"} #create kafka topic

kafkaModule.Producer(create_topic, create_data)
kafkaModule.Producer(create_topic2, create_data)