#!/usr/bin/python3
# Batch process
import seed
def stream_users_in_batches(batch_size):
    """Yield users in batches of given size."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Process each batch and filter users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user['age']) > 25:
                print(user)