from Config.schema_setup import SchemaSetup
from Data.sample_data import insert_sample_data

def reset_database(with_data=True):
    print("⚙️ Resetting database...")
    
    schema = SchemaSetup()
    schema.create_all_tables()

    print("✅ Tables created.")

    if with_data:
        insert_sample_data()

if __name__ == "__main__":
    reset_database()
