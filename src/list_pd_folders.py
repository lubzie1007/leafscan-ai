import os

base = "data/plantdoc_clean/train"
folders = sorted(os.listdir(base))

print(f"PlantDoc has {len(folders)} classes:\n")
for f in folders:
    count = len(os.listdir(os.path.join(base, f)))
    print(f'    "{f}": "",  # {count} images')