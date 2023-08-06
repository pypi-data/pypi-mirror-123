import csv
import psycopg2

def create_error_reports(domain_id, unregistered, unregistered_unique):
    print("raport nr 1")
    with open('unregister_full.csv', mode='w') as csv_file:
        fieldnames = ['url', 'uid', 'created']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in unregistered:
            writer.writerow({'url': item['url'], 'uid': item['uid'], 'created': item['createdAt']})

    """
    unregister - unique uid
    """
    print("raport nr 2")
    print(unregistered_unique)
    with open('unregister_only_uid.csv', mode='w') as csv_file:
        fieldnames = ['uid']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in unregistered_unique:
            writer.writerow({'uid': item})

    """
    postgres
    """
    still_active = []

    result = urlparse(os.environ['REAKTION_DB'])
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    cur = conn.cursor()

    for item in unregistered_unique:
        q = f"SELECT is_active from subscriptions where email_id = {item} and domain_id = {domain_id}"
        cur.execute(q)
        data = cur.fetchall()
        for d in data:
            print(d[0])
            if d[0] is True:
                print(item)
                q2 = f"SELECT email from emails where id = {item}"
                cur.execute(q2)
                data_email = cur.fetchall()
                for e in data_email:
                    still_active.append(e[0])

    conn.close()

    final_csv_name = f"unregister_emails_{domain_id}.csv"

    with open(final_csv_name, mode='w') as csv_file:
        fieldnames = ['email']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for item in still_active:
            writer.writerow({'email': item})

    print("Reports created")