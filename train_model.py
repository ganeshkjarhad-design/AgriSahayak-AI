"""
AgriSahayak AI image classifier.
Expected directory:
data/PlantVillage/<class_name>/*.jpg

For a college demo, select a manageable subset of classes first.
The script uses MobileNetV2 transfer learning.
"""
from pathlib import Path
import json, tensorflow as tf
from tensorflow.keras import layers

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"/"PlantVillage"
OUT=ROOT/"model"
OUT.mkdir(exist_ok=True)

IMG_SIZE=(224,224)
BATCH=32
SEED=42

if not DATA.exists():
    raise SystemExit("Dataset folder not found. Put PlantVillage class folders in data/PlantVillage/")

train_ds=tf.keras.utils.image_dataset_from_directory(
    DATA, validation_split=0.2, subset="training", seed=SEED,
    image_size=IMG_SIZE, batch_size=BATCH)
val_ds=tf.keras.utils.image_dataset_from_directory(
    DATA, validation_split=0.2, subset="validation", seed=SEED,
    image_size=IMG_SIZE, batch_size=BATCH)

class_names=train_ds.class_names
(Path(OUT/"class_names.json")).write_text(json.dumps(class_names, indent=2))

AUTOTUNE=tf.data.AUTOTUNE
train_ds=train_ds.prefetch(AUTOTUNE)
val_ds=val_ds.prefetch(AUTOTUNE)

base=tf.keras.applications.MobileNetV2(
    input_shape=IMG_SIZE+(3,), include_top=False, weights="imagenet")
base.trainable=False

inputs=tf.keras.Input(shape=IMG_SIZE+(3,))
x=tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
x=base(x, training=False)
x=layers.GlobalAveragePooling2D()(x)
x=layers.Dropout(0.25)(x)
outputs=layers.Dense(len(class_names), activation="softmax")(x)
model=tf.keras.Model(inputs,outputs)

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
callbacks=[tf.keras.callbacks.EarlyStopping(patience=3,restore_best_weights=True),
           tf.keras.callbacks.ModelCheckpoint(OUT/"agrisaahayak_model.keras",save_best_only=True)]

model.fit(train_ds, validation_data=val_ds, epochs=10, callbacks=callbacks)
print("Saved model and class names.")
