import os

import pandas as pd
from keras import layers
from keras.layers import TextVectorization
from sklearn import preprocessing
import tensorflow as tf
import argparse

from sklearn.model_selection import train_test_split


def store_text_vectorizer(vectorizer: TextVectorization, file_path: str):
    # Create model.
    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
    model.add(vectorizer)

    # Save.
    model.save(file_path, save_format="tf")


def load_csv(file: str) -> pd.DataFrame:
    df = pd.read_csv(file, index_col=False)
    df.rename(
        {col: col.lower().strip() for col in df.columns}, inplace=True, axis="columns"
    )
    return df


def load_dataset(path: str):
    lang_list = ["es", "en", "de"]
    if not os.path.exists(path):
        raise FileNotFoundError("Input directory %s does not exists" % path)
    if not os.path.isdir(path):
        raise ValueError("%s must be a directory" % path)

    csv_files = [
        os.path.join(path, file)
        for file in os.listdir(path)
        if file.lower().endswith(".csv")
    ]
    print("load", csv_files)

    df = pd.concat([load_csv(file) for file in csv_files], axis=0, ignore_index=True)
    df = df.loc[df.labels.isin(lang_list)]
    print(df.columns)
    train_test, val_df = train_test_split(df, test_size=0.2, stratify=df["labels"])
    train_df, test_df = train_test_split(
        train_test, test_size=0.25, stratify=train_test["labels"]
    )

    return train_df, val_df, test_df


parser = argparse.ArgumentParser()
parser.add_argument("--epochs", default=10, type=int, help="Number of training epochs")
parser.add_argument(
    "--output",
    required=True,
    type=str,
    help="Output directory for the traied model files",
)
parser.add_argument(
    "--input", default="data", type=str, help="Input directory with training csv files."
)

args = parser.parse_args()

if os.path.exists(args.output) and not os.path.isdir(args.output):
    raise ValueError("%s must be a directory" % args.output)

if not os.path.exists(args.output):
    os.mkdir(args.output)

# Select only "en", "es" and "de"
lang_list = ["es", "en", "de"]

train_df, val_df, test_df = load_dataset(args.input)

le = preprocessing.LabelEncoder()
le.fit(lang_list)

num_classes = len(le.classes_)

train_labels = tf.keras.utils.to_categorical(
    le.transform(train_df.pop("labels")), num_classes=num_classes
)
val_labels = tf.keras.utils.to_categorical(
    le.transform(val_df.pop("labels")), num_classes=num_classes
)
test_labels = tf.keras.utils.to_categorical(
    le.transform(test_df.pop("labels")), num_classes=num_classes
)

raw_train_ds = tf.data.Dataset.from_tensor_slices(
    (train_df["text"].to_list(), train_labels)
)  # X, y
raw_val_ds = tf.data.Dataset.from_tensor_slices((val_df["text"].to_list(), val_labels))
raw_test_ds = tf.data.Dataset.from_tensor_slices(
    (test_df["text"].to_list(), test_labels)
)

max_features = 10000  # top 10K most frequent words
sequence_length = 50  # We defined it in the previous data exploration section

vectorize_layer = layers.TextVectorization(
    standardize="lower_and_strip_punctuation",
    max_tokens=max_features,
    output_mode="int",
    output_sequence_length=sequence_length,
)

# train_text = train_ds.map(lambda x, y: x)
vectorize_layer.adapt(
    train_df["text"].to_list()
)  # vectorize layer is fitted to the training data

train_ds = raw_train_ds.map(
    lambda x, y: (vectorize_layer(x), y)
)  # returns vectorize_layer(text), label
val_ds = raw_val_ds.map(lambda x, y: (vectorize_layer(x), y))
test_ds = raw_test_ds.map(lambda x, y: (vectorize_layer(x), y))


# Applying cache techniques for improving inference and training time
# It allows tensorflow to prepare the data while it trains the model

AUTOTUNE = tf.data.AUTOTUNE

batch_size = 32
seed = 42

train_ds = train_ds.batch(batch_size=batch_size)
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.batch(batch_size=batch_size)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.batch(batch_size=batch_size)
test_ds = test_ds.prefetch(AUTOTUNE)

embedding_dim = 16
model = tf.keras.Sequential(
    [
        layers.Embedding(max_features + 1, embedding_dim),
        layers.Dropout(0.2),
        layers.GlobalAveragePooling1D(),
        layers.Dropout(0.2),
        layers.Dense(3),
    ]
)

model.summary()

model.compile(
    loss=tf.losses.CategoricalCrossentropy(from_logits=True, label_smoothing=0.1),
    optimizer="adam",
    metrics=["accuracy"],
)

history = model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)

loss, accuracy = model.evaluate(test_ds)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

model.save(os.path.join(args.output, "simple_mlp_novectorize.h5"))
store_text_vectorizer(vectorize_layer, os.path.join(args.output, "vectorizer"))
