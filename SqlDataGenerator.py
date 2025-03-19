import random
import string
import time
from datetime import datetime, timedelta

from Data.Names.femaleNames import female_names
from Data.Names.maleNames import male_names
from Data.Names.lastNames import last_names

from Data.Email.emailDomains import email_domains

# --------------- Constants ---------------#

COLUMN_TYPES = {
    "num": "Random Number",
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

    if row_type in ["num", "str", "date"]:
        min_val, max_val, decimal_places = get_min_max(row_type)
        return {
            "name": name,
            "type": row_type,
            "min": min_val,
            "max": max_val,
            "decimal": decimal_places,
        }

    elif row_type == "list":
        print(
            "Enter your list of values separated by commas and without spaces (unless you want it)"
        )
        lst = [item.strip() for item in input("Your elements: ").split(",")]
        return {"name": name, "type": row_type, "list": lst}

    elif row_type in ["fullname", "fname", "lname", "email", "phone", "bool"]:
        return {"name": name, "type": row_type}

    else:
        print("Invalid column type. Try again.")
        return None


def get_min_max(row_type):
    decimal_places = None
    while True:
        try:
            if row_type == "num":
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
    min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
    max_date = datetime.strptime(max_date_str, "%Y-%m-%d")
    delta = max_date - min_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return min_date + timedelta(seconds=random_seconds)


def generate_value(column):
    if column["type"] == "num":
        if isinstance(column["min"], int) and isinstance(column["max"], int):
            return str(random.randint(column["min"], column["max"]))
        else:
            return str(
                round(random.uniform(column["min"], column["max"]), column["decimal"])
            )

    elif column["type"] == "string":
        length = random.randint(column["min"], column["max"])
        return str("".join(random.choices(string.ascii_lowercase, k=length)))

    elif column["type"] == "date":
        return str(generate_datetime(column["min"], column["max"]))

    elif column["type"] == "list":
        return str(random.choice(column["list"]))

    elif column["type"] == "fullname":
        return str(
            random.choice(male_names + female_names) + " " + random.choice(last_names)
        )

    elif column["type"] == "fname":
        return str(random.choice(male_names + female_names))

    elif column["type"] == "rln":
        return str(random.choice(last_names))

    elif column["type"] == "email":
        return str(
            random.choice(male_names + female_names)
            + "."
            + random.choice(last_names)
            + random.choice(email_domains)
        )

    elif column["type"] == "phone":
        return str(
            "0"
            + str(random.randint(1, 7))
            + "".join(random.choices(string.digits, k=8))
        )

    elif column["type"] == "bool":
        return str(random.randint(0, 1))


def create_table(table_name, columns, row_count):
    start_time = time.time()

    column_names = ", ".join(col["name"] for col in columns)

    with open("data.sql", "w") as f:
        for _ in range(row_count):
            try:
                values = ", ".join(generate_value(col) for col in columns)
                query = (
                    f"INSERT INTO `{table_name}` ({column_names}) VALUES ({values});\n"
                )
                f.write(query)
            except UnicodeEncodeError as e:
                print(f"Encode Error with: {values}")
                print(f"Error: {e}")
                continue

    print_section("SQL File Created")
    end_time = time.time()
    print(f"[TIME] {end_time - start_time}")


start()
