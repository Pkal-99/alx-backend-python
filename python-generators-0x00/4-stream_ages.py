#!/usr/bin/python3
""" Memory-efficient """
import seed

def stream_user_ages():
    """Yield ages one by one from user_data table."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()

def calculate_average_age():
    """Compute average age using generator."""
    total = 0
    count = 0

    for age in stream_user_ages():
        total += int(age)
        count += 1

    avg = total / count if count else 0
    print(f"Average age of users: {avg:.2f}")


if __name__ == "__main__":
    calculate_average_age()