import psycopg2

conn = psycopg2.connect(host="localhost", user="{username}", password="{password}",
                        dbname="{dbname}", port="{port}")
cursor = conn.cursor()

#! 삽입
def insert(iot_device_uri, ai_model_name, process_id):
    cursor.execute('INSERT INTO aiaas_request (iot_device_uri, ai_model_name, process_id) VALUES(%s, %s, %s)', (iot_device_uri, ai_model_name, process_id))
    conn.commit()

#! 조회
def discovery():
    cursor.execute('select * from aiaas_request');
    res = cursor.fetchall()
    return res

#! 전체 삭제
def delete_all():
    cursor.execute('delete from aiaas_request')
    conn.commit()
    cursor.execute('select * from aiaas_request');
    res = cursor.fetchall()
    print(res)

#! 선택 삭제
def delete(process_id):
    #따옴표 써야 함 주의
    cursor.execute('delete from aiaas_request where process_id = \''+process_id+'\'')
    conn.commit()

if __name__ == "__main__":
    print(discovery())
    delete_all()
    print(discovery())