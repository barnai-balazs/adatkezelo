from faker import Faker
from basic.model_dataclasses import Person, Bicycle, Laptop
import random


def generate_people(n: int, male_ratio: float = 0.5,
                    locale: str = "en_US",
                    unique: bool = False,
                    min_age: int = 0,
                    max_age: int = 100) -> list[Person]:

    assert n > 0
    assert 0 <= male_ratio <= 1
    assert 0 <= min_age <= max_age <= 100

    people = []
    fake = Faker(locale)
    fake = fake if not unique else fake.unique

    for i in range(n):
        male = random.random() < male_ratio
        person = Person(
            id=f"P-{str(i + 1).zfill(6)}",
            name=fake.name_male() if male else fake.name_female(),
            age=random.randint(min_age, max_age),
            male=male
        )
        # Kapcsolatok inicializálása
        person.bicycles = []
        person.laptops = []
        people.append(person)

    return people


def generate_bicycles(n: int, people: list[Person]) -> list[Bicycle]:
    """Kerékpárok generálása és hozzárendelése emberekhez (1:N kapcsolat)."""
    assert n > 0 and len(people) > 0

    bicycles = []
    fake = Faker()
    bicycle_brands = ["Trek", "Specialized", "Giant", "Cannondale", "Scott", "Bianchi", "Merida", "Cube"]

    for i in range(n):
        owner = random.choice(people)
        bicycle = Bicycle(
            id=f"B-{str(i + 1).zfill(6)}",
            brand=random.choice(bicycle_brands),
            model=fake.word().capitalize() + "-" + str(random.randint(100, 999)),
            year=random.randint(2000, 2025),
            owner_id=owner.id,
        )
        # kapcsolat mindkét irányba
        bicycle.owner = owner
        owner.bicycles.append(bicycle)
        bicycles.append(bicycle)

    return bicycles


def generate_laptops(n: int, people: list[Person]) -> list[Laptop]:
    """Laptopok generálása és hozzárendelése emberekhez (1:N kapcsolat)."""
    assert n > 0 and len(people) > 0

    laptops = []
    fake = Faker()
    laptop_brands = ["Dell", "HP", "Lenovo", "Apple", "Asus", "Acer", "MSI", "Razer"]

    for i in range(n):
        owner = random.choice(people)
        laptop = Laptop(
            id=f"L-{str(i + 1).zfill(6)}",
            brand=random.choice(laptop_brands),
            model=fake.word().capitalize() + "-" + str(random.randint(100, 9999)),
            year=random.randint(2015, 2025),
            ram=random.choice([4, 8, 16, 32, 64, 128]),
            vram=random.choice([2, 4, 6, 8, 12, 16]),
            owner_id=owner.id,     # fájlkezeléshez szükséges
        )
        # kapcsolat mindkét irányba
        laptop.owner = owner
        owner.laptops.append(laptop)
        laptops.append(laptop)

    return laptops


# ------------------- Tesztelés -------------------
if __name__ == "__main__":
    people = generate_people(50, male_ratio=0.5, min_age=18, max_age=60)
    bicycles = generate_bicycles(30, people)
    laptops = generate_laptops(30, people)

    print("\n=== KAPCSOLATOK ===")
    for p in people:
        print(f"{p.name}:")
        print("  Biciklik:", [b.model for b in p.bicycles])
        print("  Laptopok:", [l.model for l in p.laptops])
        print()
