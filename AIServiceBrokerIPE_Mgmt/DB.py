import psycopg2

conn = psycopg2.connect(host="{ip}", user="yujin", password="{password}",
                        dbname="aistar", port="{port}")
cursor = conn.cursor()

#! 삽입
def insert(iot_device_uri, ai_model_name, process_id):
    try:
        cursor.execute('INSERT INTO aiaas_request (iot_device_uri, ai_model_name, process_id) VALUES(%s, %s, %s)', 
                        (iot_device_uri, ai_model_name, process_id))
        conn.commit()
    except Exception as e:
        print("Error in insert operation: ", e)
        

#! 조회
def discovery():
    cursor.execute('select * from aiaas_request')
    try:
        res = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        print("No results to fetch.")
        res = []
    return res


#! 전체 삭제
def delete_all():
    try:
        cursor.execute('delete from aiaas_request')
        conn.commit()
        cursor.execute('select * from aiaas_request');
        res = cursor.fetchall()
        print(res)
    except Exception as e:
        print("Error in delete_all operation: ", e)
        

#! 선택 삭제
def delete(process_id):
    try:
        cursor.execute('delete from aiaas_request where process_id = \''+process_id+'\'')
        conn.commit()
    except Exception as e:
        print("Error in delete operation: ", e)
        

if __name__ == "__main__":
    print(discovery())
    delete_all()