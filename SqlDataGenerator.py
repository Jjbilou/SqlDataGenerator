import random
import string
import time
from datetime import datetime, timedelta

from Data.Names.femaleNames import female_names
from Data.Names.maleNames import male_names
from Data.Names.lastNames import last_names

from Data.Email.emailDomains import email_domains

#--------------- Constants ---------------#

COLUMN_TYPES = {
    "rn": "Random Number",
    "rs": "Random String",
    "rd": "Random Date",
    "rl": "Random from List",
    "rfln": "Random Full Name",
    "rfin": "Random First Name",
    "rln": "Random Last Name",
    "re": "Random Email",
    "rp": "Random Phone Number",
    "b": "Boolean"
}

#--------------- Style ---------------#

def print_title(text):
    print("=" * 50)
    print(f"{text.center(50)}")
    print("=" * 50)

def print_section(text):
    print(f"\n{text.center(50, '-')}")

#--------------- Generator ---------------#

def start():
    print_title("SQL Data Generator")
    
    table_name = input("The name of your table: ").strip()
    columns = []
    
    while input("Create a new column? (y/n): ").lower() == "y":
        column = create_column()
        if column:
            columns.append(column)

    row_count = int(input("Number of rows to generate: "))
    create_table(table_name, columns, row_count)
    print_section("Data generation complete! Check 'data.sql'")

def create_column():
    print_section("Define a New Column")
    name = input("Column Name: ").strip()
    print_title("Column types")
    
    for key, value in COLUMN_TYPES.items():
        print(f" • {value} ({key})")
    print("=" * 50)

    row_type = input("Column Type: ").lower().strip()
    
    if row_type in ["rn", "rs", "rd"]:
        min_val, max_val = get_min_max(row_type)
        return {"name": name, "type": row_type, "min": min_val, "max": max_val}
    
    elif row_type == "rl":
        print("Enter your list of values separated by commas and without spaces (unless you want it)")
        lst = [item.strip() for item in input("Your elements: ").split(",")]
        return {"name": name, "type": row_type, "list": lst}
    
    elif row_type in ["rfln", "rfin", "rln", "re", "rp", "b"]:
        return {"name": name, "type": row_type}
    
    else:
        print("Invalid column type. Try again.")
        return None

def get_min_max(row_type):
    while True:
        try:
            if row_type == "rn":
                min_val = int(input("Min value: "))
                max_val = int(input("Max value: "))
            
            elif row_type == "rd":
                print("Date format: yyyy-mm-dd")
                min_val = input("Min date: ").strip()
                max_val = input("Max date: ").strip()
            
            else:
                min_val = int(input("Min letters: "))
                max_val = int(input("Max letters: "))

            if min_val > max_val:
                raise ValueError("Min value must be <= Max value.")
            
            return min_val, max_val

        except ValueError as e:
            print(f"Invalid input: {e}")

def generate_datetime(min_date_str, max_date_str):
    min_date = datetime.strptime(min_date_str, '%Y-%m-%d')
    max_date = datetime.strptime(max_date_str, '%Y-%m-%d')
    delta = max_date - min_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return min_date + timedelta(seconds=random_seconds)

def generate_value(column):
    if column["type"] == "rn":
        return str(random.randint(column["min"], column["max"]))
    
    elif column["type"] == "rs":
        length = random.randint(column["min"], column["max"])
        return str(''.join(random.choices(string.ascii_lowercase, k=length)))
    
    elif column["type"] == "rd":
        return str(generate_datetime(column['min'], column['max']))
    
    elif column["type"] == "rl":
        return str(random.choice(column['list']))
    
    elif column["type"] == "rfln":
        return str(random.choice([random.choice(male_names), random.choice(female_names)]) + " " + random.choice(last_names))
    
    elif column["type"] == "rfin":
        return str(random.choice([random.choice(male_names), random.choice(female_names)]))
    
    elif column["type"] == "rln":
        return str(random.choice(last_names))
    
    elif column["type"] == "rln":
        return str(random.choice(last_names))
    
    elif column["type"] == "re":
        return str(
            random.choice(
                [random.choice(male_names), random.choice(female_names)]
            )
            + "."
            + random.choice(last_names)
            + random.choice(email_domains)
        )

    elif column["type"] == "rp":
        return str("0" + str(random.randint(1, 7)) + "".join(random.choices(string.digits, k=8)))
    
    elif column["type"] == "b":
        return str(random.randint(0, 1))

def create_table(table_name, columns, row_count):
    start_time = time.time()

    column_names = ", ".join(col["name"] for col in columns)
    
    with open("data.sql", "w") as f:
        for _ in range(row_count):
            try:
                values = ", ".join(generate_value(col) for col in columns)
                query = f"INSERT INTO `{table_name}` ({column_names}) VALUES ({values});\n"
                f.write(query)
            except UnicodeEncodeError as e:
                print(f"Encode Error with: {values}")
                print(f"Error: {e}")
                continue
    
    print_section("SQL File Created")
    end_time = time.time()
    print(f"[TIME] {end_time - start_time}")

start()