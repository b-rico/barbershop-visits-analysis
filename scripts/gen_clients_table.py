"""
File Name: gen_clients_table.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This script generates a clients_table.csv file containing information for 1000 clients.
    The client data includes salutation, first name, middle initial, last name, date of birth,
    phone number, address, city, state, and zip code.
    
    The generated CSV file is saved in the specified data directory.
Args: 
    - data_dir (str): The directory where the clients_table.csv file will be saved.
Output:
    - A CSV file named 'clients_table.csv' saved to the specified data directory.
"""

import pandas as pd
import numpy as np
import os
from faker import Faker

fake = Faker()
np.random.seed(42)

def gen_clients_table(data_dir):
    """
    Generate a clients_table.csv for 1000 clients.
    Saves the clients_table.csv into data_dir.
    """

    num_clients = 1000
    client_ids = range(1, num_clients + 1)

    clients_data = []
    for client_id in client_ids:
        salutation = np.random.choice(['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Mx.'])
        first_name = fake.first_name()
        middle_initial = fake.random_element([None, fake.random_letter().upper()])
        last_name = fake.last_name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
        phone_number = fake.basic_phone_number()
        address = fake.street_address()
        city = 'Houston'
        state = 'TX'
        zip_code = fake.zipcode()

        clients_data.append({
            'id': client_id,
            'salutation': salutation,
            'first_name': first_name,
            'middle_initial': middle_initial,
            'last_name': last_name,
            'dob': dob,
            'phone_number': phone_number,
            'address': address,
            'city': city,
            'state': state,
            'zip': zip_code
        })

    clients_df = pd.DataFrame(clients_data)

    os.makedirs(data_dir, exist_ok=True)

    clients_output_path = os.path.join(data_dir, 'clients_table.csv')
    clients_df.to_csv(clients_output_path, index=False)

    print(f"Clients table CSV saved to: {clients_output_path}")

if __name__ == "__main__":
    gen_clients_table("./data")
