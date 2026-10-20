import os
import shutil

PV_DIR = "data/plantvillage/raw/color"
PD_DIR = "data/plantdoc_clean/train"
OUT_DIR = "data/merged/train"

# Exact mapping from PlantDoc folders to PlantVillage folders
MAPPING = {
    "Apple_Scab_Leaf": "Apple___Apple_scab",
    "Apple_leaf": "Apple___healthy",
    "Apple_rust_leaf": "Apple___Cedar_apple_rust",
    "Bell_pepper_leaf": "Pepper,_bell___healthy",
    "Bell_pepper_leaf_spot": "Pepper,_bell___Bacterial_spot",
    "Corn_Gray_leaf_spot": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_leaf_blight": "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_rust_leaf": "Corn_(maize)___Common_rust_",
    "Potato_leaf_early_blight": "Potato___Early_blight",
    "Potato_leaf_late_blight": "Potato___Late_blight",
    "Squash_Powdery_mildew_leaf": "Squash___Powdery_mildew",
    "Strawberry_leaf": "Strawberry___healthy",
    "Tomato_Early_blight_leaf": "Tomato___Early_blight",
    "Tomato_Septoria_leaf_spot": "Tomato___Septoria_leaf_spot",
    "Tomato_leaf": "Tomato___healthy",
    "Tomato_leaf_bacterial_spot": "Tomato___Bacterial_spot",
    "Tomato_leaf_late_blight": "Tomato___Late_blight",
    "Tomato_leaf_mosaic_virus": "Tomato___Tomato_mosaic_virus",
    "Tomato_leaf_yellow_virus": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato_mold_leaf": "Tomato___Leaf_Mold",
    "Tomato_two_spotted_spider_mites_leaf": "Tomato___Spider_mites Two-spotted_spider_mite",
    "grape_leaf": "Grape___healthy",
    "grape_leaf_black_rot": "Grape___Black_rot",
}

pv_classes = sorted([d for d in os.listdir(PV_DIR) if os.path.isdir(os.path.join(PV_DIR, d))])

print("1. Copying all PlantVillage images...")
for cls in pv_classes:
    src = os.path.join(PV_DIR, cls)
    dst = os.path.join(OUT_DIR, cls)
    shutil.copytree(src, dst, dirs_exist_ok=True)
print(f"   -> Copied {len(pv_classes)} classes.")

print("\n2. Copying & Mapping PlantDoc images...")
pd_count = 0
for pd_cls, pv_cls in MAPPING.items():
    pd_path = os.path.join(PD_DIR, pd_cls)
    if not os.path.exists(pd_path):
        print(f"   ⚠️ Warning: {pd_path} not found.")
        continue
        
    dst = os.path.join(OUT_DIR, pv_cls)
    os.makedirs(dst, exist_ok=True)
    
    for f in os.listdir(pd_path):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Prefix with 'pd_' to avoid any filename collisions
            shutil.copy2(os.path.join(pd_path, f), os.path.join(dst, f"pd_{f}"))
            pd_count += 1

print(f"\n✅ Merged successfully! Added {pd_count} PlantDoc images to the dataset.")
print(f"📂 New dataset is ready at: {OUT_DIR}")