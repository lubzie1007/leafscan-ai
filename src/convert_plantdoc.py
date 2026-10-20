import os
import duckdb
from PIL import Image
from io import BytesIO

SRC = "data/plantdoc_hf/data"
DST = "data/plantdoc_clean/train"

os.makedirs(DST, exist_ok=True)

print("Connecting to Parquet files via DuckDB...")
con = duckdb.connect()

parquet_files = [os.path.join(SRC, f) for f in os.listdir(SRC) if f.endswith(".parquet")]
files_str = ", ".join([f"'{f}'" for f in parquet_files])

query = f"SELECT * FROM read_parquet([{files_str}])"
df = con.execute(query).fetchdf()

print(f"Loaded {len(df)} images.\n")

count = 0
for idx, row in df.iterrows():
    # FIXED: Use 'class_label' instead of 'label'
    label_name = str(row['class_label']).replace(" ", "_").replace("/", "_")
    
    cls_dir = os.path.join(DST, label_name)
    os.makedirs(cls_dir, exist_ok=True)
    
    img_bytes = row['image']
    if isinstance(img_bytes, dict) and 'bytes' in img_bytes:
        img_bytes = img_bytes['bytes']
        
    img = Image.open(BytesIO(img_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")
        
    img_path = os.path.join(cls_dir, f"{idx}.jpg")
    img.save(img_path)
    count += 1
    
    if count % 500 == 0:
        print(f"Processed {count} images...")

print(f"\n✅ Saved {count} PlantDoc images to {DST}")