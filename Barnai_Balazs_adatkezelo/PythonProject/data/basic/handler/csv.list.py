import csv
import os
from typing import Type
from basic import generator
from basic.model_dataclasses import Person, Bicycle, Laptop


#  KAPCSOLATOK
def link_people_with_items(people: list[Person],
                           bicycles: list[Bicycle],
                           laptops: list[Laptop]) -> None:

    people_by_id = {p.id: p for p in people}

    for b in bicycles:
        owner = people_by_id.get(b.owner_id)
        if owner:
            b.owner = owner
            owner.bicycles.append(b)

    for l in laptops:
        owner = people_by_id.get(l.owner_id)
        if owner:
            l.owner = owner
            owner.laptops.append(l)


#  PERSON
def write_people(people: list[Person],
                 path: str,
                 file_name: str = "people_csv_list.csv",
                 delimiter: str = ";") -> None:
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name), "w", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        #  fejlécsor
        writer.writerow(["id", "name", "age", "male"])
        for person in people:
            writer.writerow([person.id, person.name, person.age, person.male])


def read_people(path: str,
                file_name: str = "people_csv_list.csv",
                delimiter: str = ";") -> list[Person]:
    with open(os.path.join(path, file_name), newline="") as file:
        rows = csv.reader(file, delimiter=delimiter)
        next(rows)  #  fejléc átugrása
        return [Person(r[0], r[1], int(r[2]), r[3].lower() in ("true", "1", "yes", "t")) for r in rows]


#  BICYCLE
def write_bicycles(bicycles: list[Bicycle],
                   path: str,
                   file_name: str = "bicycles_csv_list.csv",
                   delimiter: str = ";") -> None:
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name), "w", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        #  fejléc
        writer.writerow(["id", "brand", "model", "year", "owner_id"])
        for b in bicycles:
            writer.writerow([b.id, b.brand, b.model, b.year, b.owner_id])


def read_bicycles(path: str,
                  file_name: str = "bicycles_csv_list.csv",
                  delimiter: str = ";") -> list[Bicycle]:
    with open(os.path.join(path, file_name), newline="") as file:
        rows = csv.reader(file, delimiter=delimiter)
        next(rows)  #  fejléc átugrása
        return [Bicycle(r[0], r[1], r[2], int(r[3]), r[4]) for r in rows]


#  LAPTOP
def write_laptops(laptops: list[Laptop],
                  path: str,
                  file_name: str = "laptops_csv_list.csv",
                  delimiter: str = ";") -> None:
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name), "w", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        #  fejléc
        writer.writerow(["id", "brand", "model", "year", "ram", "vram", "owner_id"])
        for l in laptops:
            writer.writerow([l.id, l.brand, l.model, l.year, l.ram, l.vram, l.owner_id])


def read_laptops(path: str,
                 file_name: str = "laptops_csv_list.csv",
                 delimiter: str = ";") -> list[Laptop]:
    with open(os.path.join(path, file_name), newline="") as file:
        rows = csv.reader(file, delimiter=delimiter)
        next(rows)  #  fejléc átugrása
        return [Laptop(r[0], r[1], r[2], int(r[3]), int(r[4]), int(r[5]), r[6]) for r in rows]


#  KÖZVETÍTŐ FÜGGVÉNYEK
def write(entities: list[object],
          path: str,
          file_name: str | None = None,
          delimiter: str = ";") -> None:
    if not entities:
        raise ValueError("Empty entity list")

    entity_type = type(entities[0])
    if entity_type is Person:
        write_people(entities, path, file_name or "people_csv_list.csv", delimiter)
    elif entity_type is Bicycle:
        write_bicycles(entities, path, file_name or "bicycles_csv_list.csv", delimiter)
    elif entity_type is Laptop:
        write_laptops(entities, path, file_name or "laptops_csv_list.csv", delimiter)
    else:
        raise TypeError(f"Unknown entity type: {entity_type}")


def read(entity_type: Type[object],
         path: str,
         file_name: str | None = None,
         delimiter: str = ";") -> list[object]:
    if entity_type is Person:
        return read_people(path, file_name or "people_csv_list.csv", delimiter)
    elif entity_type is Bicycle:
        return read_bicycles(path, file_name or "bicycles_csv_list.csv", delimiter)
    elif entity_type is Laptop:
        return read_laptops(path, file_name or "laptops_csv_list.csv", delimiter)
    else:
        raise TypeError(f"Unknown entity type: {entity_type}")


#  TESZT FUTTATÁS
if __name__ == "__main__":
    save_path = "C:/hallgato"

    people = generator.generate_people(50)
    bicycles = generator.generate_bicycles(30, people)
    laptops = generator.generate_laptops(30, people)

    link_people_with_items(people, bicycles, laptops)

    write(people, save_path)
    write(bicycles, save_path)
    write(laptops, save_path)

    people_read = read(Person, save_path)
    bicycles_read = read(Bicycle, save_path)
    laptops_read = read(Laptop, save_path)
    link_people_with_items(people_read, bicycles_read, laptops_read)

    print("\n=== PEOPLE & THEIR ITEMS ===")
    for p in people_read:
        print(f"{p.name}:")
        print("  Biciklik:", [b.model for b in p.bicycles])
        print("  Laptopok:", [l.model for l in p.laptops])
