import oracledb
from typing import Type, cast

from basic.generator import generate_people, generate_bicycles, generate_laptops
from basic.model_dataclasses import Person, Bicycle, Laptop
from oracledb import Connection, DatabaseError



# PERSON ÍRÁSA


def write_people(people: list[Person],
                 connection: Connection,
                 table_name: str = "people",
                 create: bool = True) -> None:

    table_name = table_name or "people"
    cursor = connection.cursor()

    if create:
        try:
            cursor.execute(f"DROP TABLE {table_name} PURGE")
        except DatabaseError:
            pass

        cursor.execute(f"""
            CREATE TABLE {table_name} (
                ID VARCHAR2(8) PRIMARY KEY,
                NAME VARCHAR2(50),
                AGE NUMBER(5),
                MALE NUMBER(1)
            )
        """)

    cursor.executemany(
        f"INSERT INTO {table_name} (id, name, age, male) VALUES (:1, :2, :3, :4)",
        [(p.id, p.name, p.age, 1 if p.male else 0) for p in people]
    )
    connection.commit()



# PERSON OLVASÁSA


def read_people(connection: Connection,
                table_name: str = "people") -> list[Person]:

    table_name = table_name or "people"
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    return [Person(r[0], r[1], int(r[2]), bool(r[3])) for r in cursor.fetchall()]



# BICYCLE ÍRÁSA


def write_bicycles(bicycles: list[Bicycle],
                   connection: Connection,
                   table_name: str = "bicycles",
                   create: bool = True) -> None:

    table_name = table_name or "bicycles"
    cursor = connection.cursor()

    if create:
        try:
            cursor.execute(f"DROP TABLE {table_name} PURGE")
        except DatabaseError:
            pass

        cursor.execute(f"""
            CREATE TABLE {table_name} (
                ID VARCHAR2(8) PRIMARY KEY,
                BRAND VARCHAR2(50),
                MODEL VARCHAR2(50),
                YEAR NUMBER(5),
                OWNER_ID VARCHAR2(8),
                CONSTRAINT fk_bike_owner FOREIGN KEY (OWNER_ID)
                    REFERENCES people(id)
                    ON DELETE CASCADE
            )
        """)

    cursor.executemany(
        f"INSERT INTO {table_name} (id, brand, model, year, owner_id) VALUES (:1, :2, :3, :4, :5)",
        [(b.id, b.brand, b.model, b.year, b.owner_id) for b in bicycles]
    )
    connection.commit()



# BICYCLE OLVASÁSA


def read_bicycles(connection: Connection,
                  table_name: str = "bicycles") -> list[Bicycle]:

    table_name = table_name or "bicycles"
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    return [Bicycle(r[0], r[1], r[2], int(r[3]), r[4]) for r in cursor.fetchall()]



# LAPTOP ÍRÁSA


def write_laptops(laptops: list[Laptop],
                  connection: Connection,
                  table_name: str = "laptops",
                  create: bool = True) -> None:

    table_name = table_name or "laptops"
    cursor = connection.cursor()

    if create:
        try:
            cursor.execute(f"DROP TABLE {table_name} PURGE")
        except DatabaseError:
            pass

        cursor.execute(f"""
            CREATE TABLE {table_name} (
                ID VARCHAR2(8) PRIMARY KEY,
                BRAND VARCHAR2(50),
                MODEL VARCHAR2(50),
                YEAR NUMBER(5),
                RAM NUMBER(5),
                VRAM NUMBER(5),
                OWNER_ID VARCHAR2(8),
                CONSTRAINT fk_laptop_owner FOREIGN KEY (OWNER_ID)
                    REFERENCES people(id)
                    ON DELETE CASCADE
            )
        """)

    cursor.executemany(
        f"""
        INSERT INTO {table_name} (id, brand, model, year, ram, vram, owner_id)
        VALUES (:1, :2, :3, :4, :5, :6, :7)
        """,
        [(l.id, l.brand, l.model, l.year, l.ram, l.vram, l.owner_id) for l in laptops]
    )
    connection.commit()



# LAPTOP OLVASÁSA


def read_laptops(connection: Connection,
                 table_name: str = "laptops") -> list[Laptop]:

    table_name = table_name or "laptops"
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    return [
        Laptop(r[0], r[1], r[2], int(r[3]), int(r[4]), int(r[5]), r[6])
        for r in cursor.fetchall()
    ]



# KÖZVETÍTŐ: WRITE()


def write(entities: list[object],
          connection: Connection,
          table_name: str = None,
          create: bool = True) -> None:

    first = entities[0]

    if isinstance(first, Person):
        return write_people(
            [cast(Person, e) for e in entities],
            connection,
            table_name=table_name,
            create=create
        )

    elif isinstance(first, Bicycle):
        return write_bicycles(
            [cast(Bicycle, e) for e in entities],
            connection,
            table_name=table_name,
            create=create
        )

    elif isinstance(first, Laptop):
        return write_laptops(
            [cast(Laptop, e) for e in entities],
            connection,
            table_name=table_name,
            create=create
        )

    raise RuntimeError("Unknown entity type")



# KÖZVETÍTŐ: READ()


def read(entity_type: Type[object],
         connection: Connection,
         table_name: str = None) -> list[object]:

    if entity_type == Person:
        return read_people(connection, table_name)

    elif entity_type == Bicycle:
        return read_bicycles(connection, table_name)

    elif entity_type == Laptop:
        return read_laptops(connection, table_name)

    raise RuntimeError("Unknown entity type")



# ORACLE BEÁLLÍTÁS


try:
    oracledb.init_oracle_client(lib_dir=r"C:\instantclient_21_7")
except:
    pass

DB_USER =                                                                                                                                                                                                                                                                                                                               "U_UI092T"
DB_PASS =                                                                                                                                                                                                                                                                                                                                                   "balazs123"

DSN = "codd.inf.unideb.hu:1521/ora21cp.inf.unideb.hu"



# KAPCSOLATOK ÚJRAÉPÍTÉSE


def rebuild_connections(people: list[Person],
                        bicycles: list[Bicycle],
                        laptops: list[Laptop]) -> None:
    """Owner_id alapján visszaállítja a kapcsolatokat."""

    people_by_id = {p.id: p for p in people}

    for p in people:
        p.bicycles = []
        p.laptops = []

    for b in bicycles:
        if b.owner_id in people_by_id:
            owner = people_by_id[b.owner_id]
            b.owner = owner
            owner.bicycles.append(b)

    for l in laptops:
        if l.owner_id in people_by_id:
            owner = people_by_id[l.owner_id]
            l.owner = owner
            owner.laptops.append(l)



# KAPCSOLATOK KIÍRÁSA


def print_connections(people: list[Person]) -> None:
    print("\n=== KAPCSOLATOK ===")
    for p in people:
        print(f"{p.name}:")
        print(f"  Biciklik: {[b.model for b in p.bicycles]}")
        print(f"  Laptopok: {[l.model for l in p.laptops]}")
        print()



def main():

    people = generate_people(50)
    bicycles = generate_bicycles(50, people)
    laptops = generate_laptops(50, people)

    print("Kapcsolódás Oracle-hez...")
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASS,
        dsn=DSN
    )
    print("Sikeres kapcsolat.")

    write(people, conn, table_name="people", create=True)
    write(bicycles, conn, table_name="bicycles", create=True)
    write(laptops, conn, table_name="laptops", create=True)

    print("Adatok beírva az adatbázisba.")

    db_people = read(Person, conn, table_name="people")
    db_bicycles = read(Bicycle, conn, table_name="bicycles")
    db_laptops = read(Laptop, conn, table_name="laptops")

    print("Adatok visszaolvasva.")

    rebuild_connections(db_people, db_bicycles, db_laptops)

    print_connections(db_people)

    conn.close()
    print("Oracle kapcsolat lezárva.")


if __name__ == "__main__":
    main()
