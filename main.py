import hashlib
import time
import psycopg2, requests, json
from datetime import datetime

swapi_root_url = "https://swapi.dev/api/"
sha256_hash = hashlib.sha256()

#TODO: Probably use a cadence service.
while True:
    conn = psycopg2.connect(
    dbname="swapi_data",
    user="test_user",
    password="user_password"
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    print("Running update...")

    try:
        root_response = requests.get(swapi_root_url)
        resources = json.loads(root_response.text)

        for resource in resources:
            create_table_query = "CREATE TABLE IF NOT EXISTS {} (id TEXT, updated TIMESTAMP, data jsonb, PRIMARY KEY (id ,updated))".format(resource)
            cur.execute(create_table_query)
            conn.commit()

        for resource in resources:
            resource_url = swapi_root_url + resource
            #TODO: Catch error codes.
            resource_response = requests.get(resource_url)
            #TODO: Iterate over all pages.
            
            #TODO: Catch json errors.
            data = json.loads(resource_response.text)

            for result in data["results"]:
                result_string = json.dumps(result)
                sha256_hash.update(result_string.encode('utf-8'))
                hashed_result = sha256_hash.hexdigest()

                #TODO: Check if hash is present in database and only insert if not.
                sql_statement = "INSERT INTO {} (id, updated, data) VALUES (%s, %s, %s)".format(resource)
                timestamp = datetime.now()
                cur.execute(sql_statement, (hashed_result, timestamp, result_string))
                conn.commit()
            
            print("Updated {} table.".format(resource))

        cur.close()
        conn.close()

        executing_period_sec = 10
        print("Finished update. Running again in {} seconds...".format(executing_period_sec))
        time.sleep(executing_period_sec)
    
    except Exception as e:
        print("An error occured: {}".format(e))

    cur.close()
    conn.close()