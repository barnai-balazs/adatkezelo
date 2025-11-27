from dataclasses import dataclass, field
from typing import Optional, Union, TYPE_CHECKING
from functools import total_ordering

if TYPE_CHECKING:
    from basic.model_dataclasses import Person, Bicycle, Laptop


@total_ordering
@dataclass(unsafe_hash=True)
class Person:
    id: str = field(hash=True)
    name: str = field(compare=False)
    age: int = field(compare=False)
    male: bool = field(compare=False, default=True)

    # Kapcsolatok
    bicycles: list["Bicycle"] = field(default_factory=list, compare=False)
    laptops: list["Laptop"] = field(default_factory=list, compare=False)

    def __lt__(self, o: object) -> bool:
        if not isinstance(o, Person):
            return NotImplemented
        return self.id < o.id

    # Segédfüggvények
    def add_bicycle(self, bicycle: "Bicycle") -> None:
        if bicycle not in self.bicycles:
            self.bicycles.append(bicycle)

    def add_laptop(self, laptop: "Laptop") -> None:
        if laptop not in self.laptops:
            self.laptops.append(laptop)


@dataclass(unsafe_hash=True)
class Bicycle:
    id: str = field(hash=True)
    brand: str = field(compare=False)
    model: str = field(compare=False)
    year: int = field(compare=False)
    owner: Optional[Union["Person", str]] = field(default=None, compare=False)
    owner_id: Optional[str] = field(default=None, compare=False)

    def __post_init__(self):

        if isinstance(self.owner, str):
            self.owner_id = self.owner
            self.owner = None

        elif self.owner is not None:
            self.owner_id = self.owner.id
            self.owner.add_bicycle(self)


@dataclass(unsafe_hash=True)
class Laptop:
    id: str = field(hash=True)
    brand: str = field(compare=False)
    model: str = field(compare=False)
    year: int = field(compare=False)
    ram: int = field(compare=False)
    vram: int = field(compare=False)
    owner: Optional[Union["Person", str]] = field(default=None, compare=False)
    owner_id: Optional[str] = field(default=None, compare=False)

    def __post_init__(self):
        if isinstance(self.owner, str):
            self.owner_id = self.owner
            self.owner = None
        elif self.owner is not None:
            self.owner_id = self.owner.id
            self.owner.add_laptop(self)



# ------------------- Tesztelés -------------------
if __name__ == "__main__":
    p1 = Person("ABC", "Aladár", 16, True)
    print()
    p2 = Person("DEF", "Béla", 18, False)

    # Tulajdonos hozzárendelése objektummal
    b1 = Bicycle("B001", "Cube", "Acid", 2020, owner=p1)
    b2 = Bicycle("B002", "Trek", "Marlin", 2021, owner=p1)
    b3 = Bicycle("B003", "Giant", "Talon", 2021, owner=p2)

    l1 = Laptop("L001", "Dell", "XPS", 2022, 16, 8, owner=p1)
    l2 = Laptop("L002", "HP", "Omen", 2023, 32, 12, owner=p2)

    print(p1)
    print("Biciklik:", [b.brand for b in p1.bicycles])
    print("Laptopok:", [l.brand for l in p1.laptops])

    print("\n" + str(p2))
    print("Biciklik:", [b.brand for b in p2.bicycles])
    print("Laptopok:", [l.brand for l in p2.laptops])
