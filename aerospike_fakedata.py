import random
import faker
from aerospikedemo.aerospike_connection import AerospikeDBConnection
from dbconfig import Config

fake = faker.Faker()
def generate_fake_hotel_data():
    hotel_data = {
        "hotel_name": fake.company() + " Hotel",
        "location": fake.city(),
        "address": fake.address(),
        "phone": fake.phone_number(),
        "email": fake.email(),
        "website": fake.url(),
        "rating": round(random.uniform(1, 5), 1),
    }
    return hotel_data

def insert_multiple_fake_hotel_data(num_hotels):
    hostname = Config.NLB_URL
    namespace = Config.NAMESPACE
    set_name = Config.SET_NAME
    db = AerospikeDBConnection(hostname=hostname,namespace=namespace,set_name=set_name)
    db.connect()
    try:
        for _ in range(num_hotels):
            fake_data = generate_fake_hotel_data()
            db.create_record(fake.uuid4(), fake_data)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.disconnect()

def main():
    hotel_data = insert_multiple_fake_hotel_data(1000)
if __name__ == "__main__":
    main()