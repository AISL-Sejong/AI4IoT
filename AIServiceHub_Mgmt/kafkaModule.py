from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps


def Producer(topic_name, data, ip = '{ip}', port = '{port}'): #모듈 기능 확인해서 사용하기
    producer = KafkaProducer(
        acks=0,
        compression_type='gzip', 
        bootstrap_servers=[ip + ':' + port], 
        value_serializer=lambda x: dumps(x).encode('utf-8')
        )

    producer.send(topic_name,value=data)
    producer.flush()


def Consumer(topic_name, ip = '{ip}', port = '{port}'): #모듈 기능 확인해서 사용하기
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[ip + ':' + port],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    for message in consumer:
        return message.value
