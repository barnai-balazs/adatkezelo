from functools import total_ordering

@total_ordering
class Person:
    id: str
    name: str
    age: int
    male: bool

    def __init__(self, id: str, name: str, age: int, male: bool = True) -> None:
        self.id = id
        self.name = name
        self.age = age
        self.male = male
        self.bicycles = []   # 1:N kapcsolat
        self.laptops = []    # 1:N kapcsolat

    def __str__(self) -> str:
        return f"#{self.id}: {self.name} ({self.age} éves, {'férfi' if self.male else 'nő'})"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Person) and self.id == o.id

    def __lt__(self, o: object) -> bool:
        if not isinstance(o, Person):
            return NotImplemented
        return self.id < o.id

    def add_bicycle(self, bicycle: "Bicycle"):
        """Hozzárendel egy biciklit a személyhez."""
        if bicycle not in self.bicycles:
            self.bicycles.append(bicycle)
            bicycle.owner = self

    def add_laptop(self, laptop: "Laptop"):
        """Hozzárendel egy laptopot a személyhez."""
        if laptop not in self.laptops:
            self.laptops.append(laptop)
            laptop.owner = self


@total_ordering
class Bicycle:
    def __init__(self, id: str, brand: str, model: str, year: int, owner: Person = None) -> None:
        self.id = id
        self.brand = brand
        self.model = model
        self.year = year
        self.owner = owner
        if owner:
            owner.add_bicycle(self)

    def __str__(self) -> str:
        owner_name = self.owner.name if self.owner else "Nincs tulaj"
        return f"#{self.id}: {self.brand} {self.model} ({self.year}) - tulaj: {owner_name}"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Bicycle) and self.id == o.id

    def __lt__(self, o: object) -> bool:
        if not isinstance(o, Bicycle):
            return NotImplemented
        return self.id < o.id


@total_ordering
class Laptop:
    def __init__(self, id: str, brand: str, model: str, year: int, ram: int, vram: int, owner: Person = None) -> None:
        self.id = id
        self.brand = brand
        self.model = model
        self.year = year
        self.ram = ram
        self.vram = vram
        self.owner = owner
        if owner:
            owner.add_laptop(self)

    def __str__(self) -> str:
        owner_name = self.owner.name if self.owner else "Nincs tulaj"
        return f"#{self.id}: {self.brand} {self.model} ({self.year}) - RAM: {self.ram}GB, VRAM: {self.vram}GB - tulaj: {owner_name}"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Laptop) and self.id == o.id

    def __lt__(self, o: object) -> bool:
        if not isinstance(o, Laptop):
            return NotImplemented
        return self.id < o.id


# ---- Tesztelés ----
if __name__ == "__main__":
    p1 = Person(id="123456AB", name="Teszt Elek", age=19)
    p2 = Person(id="654321CD", name="Teszt Béla", age=22, male=False)

    b1 = Bicycle("B001", "Cube", "Acid", 2020, owner=p1)
    b2 = Bicycle("B002", "Trek", "Marlin", 2019, owner=p1)
    b3 = Bicycle("B003", "Giant", "Talon", 2021, owner=p2)

    l1 = Laptop("L001", "Dell", "XPS", 2022, 16, 8, owner=p1)
    l2 = Laptop("L002", "HP", "Omen", 2021, 32, 12, owner=p2)

    print(p1)
    print("Biciklik:", [b.brand for b in p1.bicycles])
    print("Laptopok:", [l.brand for l in p1.laptops])
    print()
    print(p2)
    print("Biciklik:", [b.brand for b in p2.bicycles])
    print("Laptopok:", [l.brand for l in p2.laptops])
