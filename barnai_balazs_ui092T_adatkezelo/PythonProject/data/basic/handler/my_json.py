import json
import os
from typing import Type
from basic import generator
from basic.model_dataclasses import Person, Bicycle, Laptop


#  KAPCSOLATOK
def link_people_with_items(people: list[Person],
                           bicycles: list[Bicycle],
                           laptops: list[Laptop]) -> None:
    """Beállítja a kapcsolatokat a beolvasott objektumok között."""
    people_by_id = {p.id: p for p in people}

    # Biciklik hozzárendelése tulajdonoshoz
    for b in bicycles:
        owner = people_by_id.get(b.owner_id)
        if owner:
            b.owner = owner
            owner.bicycles.append(b)

    # Laptopok hozzárendelése tulajdonoshoz
    for l in laptops:
        owner = people_by_id.get(l.owner_id)
        if owner:
            l.owner = owner
            owner.laptops.append(l)


#  ÍRÁS / OLVASÁS
def write_people(people: list[Person],
                 path: str,
                 file_name: str | None = None,
                 extension: str | None = None,
                 pretty: bool = True) -> None:
    file_name = file_name or "people"
    extension = extension or ".json"
    full_path = os.path.join(path, file_name + extension)

    os.makedirs(path, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as file:
        data = [p.__dict__.copy() for p in people]
        for d in data:
            d.pop("bicycles", None)
            d.pop("laptops", None)
        json.dump(data, file, indent=2 if pretty else None, ensure_ascii=False)


def read_people(path: str,
                file_name: str | None = None,
                extension: str | None = None) -> list[Person]:
    file_name = file_name or "people"
    extension = extension or ".json"
    full_path = os.path.join(path, file_name + extension)

    with open(full_path, encoding="utf-8") as file:
        objects = json.load(file)
        return [Person(obj["id"], obj["name"], int(obj["age"]), obj["male"]) for obj in objects]


def write_bicycles(bicycles: list[Bicycle],
                   path: str,
                   file_name: str | None = None,
                   extension: str | None = None,
                   pretty: bool = True) -> None:
    file_name = file_name or "bicycles"
    extension = extension or ".json"
    full_path = os.path.join(path, file_name + extension)

    os.makedirs(path, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as file:
        data = [b.__dict__.copy() for b in bicycles]
        for d in data:
            if not isinstance(d["owner_id"], str):
                d["owner_id"] = d["owner"].id if d["owner"] else None
            d.pop("owner", None)
        json.dump(data, file, indent=2 if pretty else None, ensure_ascii=False)


def read_bicycles(path: str,
                  file_name: str | None = None,
                  extension: str | None = None) -> list[Bicycle]:
    file_name = file_name or "bicycles"
    extension = extension or ".json"
    full_path = os.path.join(path, file_name + extension)

    with open(full_path, encoding="utf-8") as file:
        objects = json.load(file)
        return [
            Bicycle(
                obj["id"],
                obj["brand"],
                obj["model"],
                int(obj["year"]),
                obj["owner_id"]
            ) for obj in objects
        ]


def write_laptops(laptops: list[Laptop],
                  path: str,
                  file_name: str | None = None,
                  extension: str | None = None,
                  pretty: bool = True) -> None:
    file_name = file_name or "laptops"
    extension = extension or ".json"
    full_path = os.path.join(path, file_name + extension)

    os.makedirs(path, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as file:
        data = [l.__dict__.copy() for l in laptops]
        for d in data:
            if not isinstance(d["owner_id"], str):
                d["owner_id"] = d["owner"].id if d["owner"] else None
            d.pop("owner", None)
        json.dump(data, file, indent=2 if pretty else None, ensure_ascii=False)


def read_laptops(path: str,
                 file_name: str | None = None,
                 extension: str | None = None) -> list[Laptop]:
    file_name = file_name or "laptops"
    extension = extension or ".json"
    full_path = os.path.join(path, file_name + extension)

    with open(full_path, encoding="utf-8") as file:
        objects = json.load(file)
        return [
            Laptop(
                obj["id"],
                obj["brand"],
                obj["model"],
                int(obj["year"]),
                int(obj["ram"]),
                int(obj["vram"]),
                obj["owner_id"]
            ) for obj in objects
        ]


#  KÖZVETÍTŐ
def write(entities: list[object],
          path: str,
          file_name: str | None = None,
          extension: str | None = None,
          pretty: bool = True) -> None:
    if not entities:
        return

    extension = extension or ".json"
    first = entities[0]

    if isinstance(first, Person):
        write_people(entities, path, file_name, extension, pretty)
    elif isinstance(first, Bicycle):
        write_bicycles(entities, path, file_name, extension, pretty)
    elif isinstance(first, Laptop):
        write_laptops(entities, path, file_name, extension, pretty)
    else:
        raise TypeError(f"Nem ismert típus: {type(first)}")


def read(entity_type: Type[object],
         path: str,
         file_name: str | None = None,
         extension: str | None = None) -> list[object]:
    if entity_type == Person:
        return read_people(path, file_name, extension)
    elif entity_type == Bicycle:
        return read_bicycles(path, file_name, extension)
    elif entity_type == Laptop:
        return read_laptops(path, file_name, extension)
    else:
        raise TypeError(f"Nem ismert típus: {entity_type}")


# TESZT FUTTATÁS
if __name__ == "__main__":
    path = "C:/hallgato"

    # Generálás
    people = generator.generate_people(50)
    bicycles = generator.generate_bicycles(30, people)
    laptops = generator.generate_laptops(30, people)

    # Kapcsolatok összerendezése
    link_people_with_items(people, bicycles, laptops)

    # Mentés
    write(people, path)
    write(bicycles, path)
    write(laptops, path)

    # Olvasás
    people_read = read(Person, path)
    bicycles_read = read(Bicycle, path)
    laptops_read = read(Laptop, path)

    # Kapcsolatok visszaépítése
    link_people_with_items(people_read, bicycles_read, laptops_read)

    # Ellenőrzés
    print("\n=== PEOPLE AND THEIR ITEMS ===")
    for p in people_read:
        print(f"{p.name} ({p.id})")
        print("  Bicycles:", [b.model for b in p.bicycles])
        print("  Laptops:", [l.model for l in p.laptops])
        print()
