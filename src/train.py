import os
import argparse
import tensorflow as tf
import keras_nlp

os.environ["KERAS_BACKEND"] = "tensorflow"

def load_corpus(data_dir):
    """
    Loads all .txt files from the data directory into a single text dataset.
    """
    text_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.txt')]
    if not text_files:
        print(f"Warning: No text files found in {data_dir}.")
        return tf.data.Dataset.from_tensor_slices([])
        
    print(f"Loading {len(text_files)} text files from {data_dir}...")
    
    # Read text files into a dataset
    dataset = tf.data.TextLineDataset(text_files)
    
    # Filter out empty lines
    dataset = dataset.filter(lambda x: tf.strings.length(tf.strings.strip(x)) > 0)
    
    return dataset

def prepare_dataset(dataset, batch_size):
    """
    Batches and prefetches the dataset for optimal training performance.
    """
    # Simply batch the raw strings - KerasNLP's Preprocessor handles tokenization
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset

def build_model():
    """
    Initializes a foundational Transformer model using KerasNLP.
    We use GPT-2 as the base, keeping the foundation layers frozen initially,
    if desired, or fine-tuning the whole model.
    """
    # Load a pre-trained basic GPT-2 model and its preprocessor
    print("Loading pre-trained GPT-2 model from KerasNLP...")
    preprocessor = keras_nlp.models.GPT2CausalLMPreprocessor.from_preset(
        "gpt2_base_en",
        sequence_length=128
    )
    
    model = keras_nlp.models.GPT2CausalLM.from_preset(
        "gpt2_base_en",
        preprocessor=preprocessor
    )
    
    # Optionally, we could freeze the embeddings or bottom layers here
    # For now, we allow the model to fully fine-tune to adopt the tone heavily
    
    # Compile the model for training
    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),
        weighted_metrics=["accuracy"]
    )
    return model

def train(epochs, batch_size, data_dir, model_save_path):
    dataset = load_corpus(data_dir)
    train_ds = prepare_dataset(dataset, batch_size)
    
    # Check if dataset is empty
    if len(list(train_ds.take(1))) == 0:
        print("Dataset is empty. Cannot start training.")
        return

    model = build_model()
    
    print("Beginning fine-tuning...")
    model.fit(train_ds, epochs=epochs)
    
    # Save the fine-tuned weights
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune The Epoch Chronicler")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size for training")
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data", "raw")
    model_save_path = os.path.join(base_dir, "models", "epoch_chronicler.keras")
    
    train(epochs=args.epochs, batch_size=args.batch_size, data_dir=data_dir, model_save_path=model_save_path)
