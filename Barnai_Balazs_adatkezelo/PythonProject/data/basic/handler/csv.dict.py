import csv
import os
from basic import generator
from basic.model_dataclasses import Person, Bicycle, Laptop


#  CSV ÍRÁS

def write_people(people: list[Person],
                 path: str,
                 file_name: str = "people_dict.csv",
                 delimiter: str = ";") -> None:
    """Emberek írása CSV-be (fejléc + adatok)"""
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "age", "male"], delimiter=delimiter)
        writer.writeheader()
        for p in people:
            writer.writerow({
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "male": p.male
            })


def write_bicycles(bicycles: list[Bicycle],
                   path: str,
                   file_name: str = "bicycles_dict.csv",
                   delimiter: str = ";") -> None:
    """Biciklik írása CSV-be"""
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "brand", "model", "year", "owner_id"], delimiter=delimiter)
        writer.writeheader()
        for b in bicycles:
            writer.writerow({
                "id": b.id,
                "brand": b.brand,
                "model": b.model,
                "year": b.year,
                "owner_id": b.owner_id
            })


def write_laptops(laptops: list[Laptop],
                  path: str,
                  file_name: str = "laptops_dict.csv",
                  delimiter: str = ";") -> None:
    """Laptopok írása CSV-be"""
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name), "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "brand", "model", "year", "ram", "vram", "owner_id"], delimiter=delimiter)
        writer.writeheader()
        for l in laptops:
            writer.writerow({
                "id": l.id,
                "brand": l.brand,
                "model": l.model,
                "year": l.year,
                "ram": l.ram,
                "vram": l.vram,
                "owner_id": l.owner_id
            })


# OLVASÁS
def read_people(path: str, file_name: str = "people_dict.csv", delimiter: str = ";") -> list[Person]:
    with open(os.path.join(path, file_name), encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return [Person(row["id"], row["name"], int(row["age"]), row["male"] == "True") for row in reader]


def read_bicycles(path: str, file_name: str = "bicycles_dict.csv", delimiter: str = ";") -> list[Bicycle]:
    with open(os.path.join(path, file_name), encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return [Bicycle(row["id"], row["brand"], row["model"], int(row["year"]), row["owner_id"]) for row in reader]


def read_laptops(path: str, file_name: str = "laptops_dict.csv", delimiter: str = ";") -> list[Laptop]:
    with open(os.path.join(path, file_name), encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return [Laptop(row["id"], row["brand"], row["model"], int(row["year"]),
                       int(row["ram"]), int(row["vram"]), row["owner_id"]) for row in reader]


#  TESZT FUTTATÁS
if __name__ == "__main__":
    save_path = "C:/hallgato"
    os.makedirs(save_path, exist_ok=True)

    # Adatgenerálás
    people = generator.generate_people(50)
    bicycles = generator.generate_bicycles(30, people)
    laptops = generator.generate_laptops(30, people)

    # Mentés CSV-be
    write_people(people, save_path)
    write_bicycles(bicycles, save_path)
    write_laptops(laptops, save_path)

    # Visszaolvasás
    people_read = read_people(save_path)
    bicycles_read = read_bicycles(save_path)
    laptops_read = read_laptops(save_path)

    #  Kapcsolatok kiírása
    print("\n=== PEOPLE & THEIR ITEMS ===")
    for person in people_read:
        # hozzárendelt biciklik és laptopok (owner_id alapján)
        person_bikes = [b.model for b in bicycles_read if b.owner_id == person.id]
        person_laptops = [l.model for l in laptops_read if l.owner_id == person.id]

        print(f"{person.name}:")
        print("  Biciklik:", person_bikes if person_bikes else "[]")
        print("  Laptopok:", person_laptops if person_laptops else "[]")
