import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# --- 1. Excel beolvasása ---
file_path = r"C:\hallgato\data_xlsx.xlsx"
df = pd.read_excel(file_path, sheet_name="laptops")

# --- 2. Átlagos RAM és VRAM gyártónként ---
avg_ram = df.groupby("brand")["ram"].mean()
avg_vram = df.groupby("brand")["vram"].mean()

# --- 3. Laptop darabszám gyártónként ---
count_by_brand = df["brand"].value_counts()

# --- PDF fájl neve ---
pdf_path = r"C:\hallgato\laptop_diagrams.pdf"


with PdfPages(pdf_path) as pdf:

    # --- RAM oszlopdiagram ---
    plt.figure(figsize=(10, 6))
    avg_ram.plot(kind="bar")
    plt.title("Átlagos RAM gyártónként (GB)")
    plt.xlabel("Gyártó")
    plt.ylabel("Átlagos RAM (GB)")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # --- VRAM SÁVDIAGRAM
    plt.figure(figsize=(10, 6))
    avg_vram.plot(kind="barh")
    plt.title("Átlagos VRAM gyártónként (GB)")
    plt.xlabel("Átlagos VRAM (GB)")
    plt.ylabel("Gyártó")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # --- Kördiagram
    plt.figure(figsize=(8, 8))
    plt.pie(
        count_by_brand,
        labels=count_by_brand.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Laptopok darabszáma gyártónként")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

print("PDF diagramok sikeresen elkészítve:", pdf_path)
