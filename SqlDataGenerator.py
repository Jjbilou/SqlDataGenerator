import random
import string
import time
from datetime import datetime, timedelta

from Data.Names.femaleNames import female_names
from Data.Names.maleNames import male_names
from Data.Names.lastNames import last_names

from Data.Email.emailDomains import email_domains

# --------------- Constants ---------------#

# Dictionary that defines the available column types and their meanings
COLUMN_TYPES = {
    "num": "Random Number",
    "uniquenum": "Unique Random Number",
    "str": "Random String",
    "date": "Random Date",
    "list": "Random from List",
    "fullname": "Random Full Name",
    "fname": "Random First Name",
    "lname": "Random Last Name",
    "email": "Random Email",
    "phone": "Random Phone Number",
    "bool": "Boolean",
}

# --------------- Style ---------------#


def print_title(text):
    print("=" * 50)
    print(f"{text.center(50)}")
    print("=" * 50)


def print_section(text):
    print(f"\n{text.center(50, '-')}")


# --------------- Generator ---------------#


def start():
    print_title("SQL Data Generator")

    table_name = input("The name of your table: ").strip()
    columns = []

    # Loop to allow the user to create multiple columns
    while input("Create a new column? (y/n): ").lower() == "y":
        column = create_column()
        if column:
            columns.append(column)

    row_count = int(input("Number of rows to generate: "))
    create_table(table_name, columns, row_count)
    print_section("Data generation complete! Check 'data.sql'")


# Return "column" who is a dictionary with the name, the type and any other specific elements
def create_column():
    print_section("Define a New Column")
    name = input("Column Name: ").strip()
    print_title("Column types")

    # Display all available column choices
    for key, value in COLUMN_TYPES.items():
        print(f" • {value} ({key})")
    print("=" * 50)

    row_type = input("Column Type: ").lower().strip()

    # Handle numeric, string, and date types, require min/max
    if row_type in ["num", "uniquenum", "str", "date"]:
        min_val, max_val, decimal_places = get_min_max(row_type)
        return {
            "name": name,
            "type": row_type,
            "min": min_val,
            "max": max_val,
            "decimal": decimal_places,
        }

    # Handle list type user-defined values
    elif row_type == "list":
        print(
            "Enter your list of values separated by commas and without spaces (unless you want it)"
        )
        lst = [item.strip() for item in input("Your elements: ").split(",")]
        return {"name": name, "type": row_type, "list": lst}

    # Handle types that don't need extra configuration
    elif row_type in ["fullname", "fname", "lname", "email", "phone", "bool"]:
        return {"name": name, "type": row_type}

    else:
        print("Invalid column type. Try again.")
        return None


def get_min_max(row_type):
    decimal_places = None
    while True:
        try:
            # if min or max or both are float, ask for decimal places.
            if row_type in ["num", "uniquenum"]:
                print(
                    "int or float, for a float at least one of the inputs must be a float"
                )
                min_val = input("Min value: ")
                max_val = input("Max value: ")
                try:
                    min_val = int(min_val)
                    max_val = int(max_val)
                except ValueError:
                    try:
                        min_val = float(min_val)
                        max_val = float(max_val)
                        decimal_places = int(
                            input("Number of decimal places (max 15): ")
                        )

                        if decimal_places < 0 or decimal_places > 15:
                            raise ValueError(
                                "Invalid number of decimal places. Must be between 0 and 15."
                            )

                    except ValueError:
                        raise ValueError("Invalid input. Please enter numeric values.")

            elif row_type == "date":
                print("Date format: yyyy-mm-dd")
                min_val = input("Min date: ").strip()
                max_val = input("Max date: ").strip()

            elif row_type == "str":
                min_val = int(input("Min letters: "))
                max_val = int(input("Max letters: "))

            if min_val > max_val:
                raise ValueError("Min value must be <= Max value.")

            return min_val, max_val, decimal_places

        except ValueError as e:
            print(f"Invalid input: {e}")


def generate_datetime(min_date_str, max_date_str):
    # Convert min and max date strings into datetime objects
    min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
    max_date = datetime.strptime(max_date_str, "%Y-%m-%d")

    # Calculate the total time difference and generate a random number of seconds within that time range
    delta = max_date - min_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return min_date + timedelta(seconds=random_seconds)

def generate_value(column, used_uniquenums):
    # If min and max are int generate a random int, esle, generate a random float
    if column["type"] == "num":
        if isinstance(column["min"], int) and isinstance(column["max"], int):
            return str(random.randint(column["min"], column["max"]))
        else:
            return str(
                round(random.uniform(column["min"], column["max"]), column["decimal"])
            )

    if column["type"] == "uniquenum":
        if isinstance(column["min"], int) and isinstance(column["max"], int):
            while True:
                value = random.randint(column["min"], column["max"])
                if value not in used_uniquenums[column["name"]]:
                    used_uniquenums[column["name"]].add(value)
                    return str(value)
        else:
            while True:
                value = round(random.uniform(column["min"], column["max"]), column["decimal"])
                if value not in used_uniquenums[column["name"]]:
                    used_uniquenums[column["name"]].add(value)
                    return str(value)

    elif column["type"] == "str":
        length = random.randint(column["min"], column["max"])
        return "".join(random.choices(string.ascii_lowercase, k=length))

    elif column["type"] == "date":
        return str(generate_datetime(column["min"], column["max"]))

    elif column["type"] == "list":
        return str(random.choice(column["list"]))

    elif column["type"] == "fullname":
        return f"{random.choice(male_names + female_names)} {random.choice(last_names)}"

    elif column["type"] == "fname":
        return str(random.choice(male_names + female_names))

    elif column["type"] == "rln":
        return str(random.choice(last_names))

    # Generate a random email like "firstname.lastname@email.domains"
    elif column["type"] == "email":
        return f"{random.choice(male_names + female_names)}.{random.choice(last_names)}{random.choice(email_domains)}"

    # Generate the two first digits between 01 and 07, the others are fully random
    elif column["type"] == "phone":
        return f"0{random.randint(1, 7)}{''.join(random.choices(string.digits, k=8))}"

    elif column["type"] == "bool":
        return str(random.randint(0, 1))


def create_table(table_name, columns, row_count):
    # Record the starting time for performance tracking
    start_time = time.time()

    # Prepare the column names
    column_names = "`, `".join(col["name"] for col in columns)

    used_uniquenums = {col["name"]: set() for col in columns if col["type"] == "uniquenum"}

    # Open the file data.sql, "w" is for
    with open("data.sql", "w") as f:
        for _ in range(row_count):
            try:
                values = "`, `".join(
                    generate_value(col, used_uniquenums) for col in columns
                )
                query = f"INSERT INTO `{table_name}` (`{column_names}`) VALUES (`{values}`);\n"
                f.write(query)
            # Error if you enter something that can't be write.
            except UnicodeEncodeError as e:
                print(f"Encode Error with: {values}")
                print(f"Error: {e}")
                continue

    print_title("SQL File Created")
    end_time = time.time()
    print(f"[TIME] : {end_time - start_time}")


start()
