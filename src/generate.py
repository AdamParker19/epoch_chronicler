import os
import argparse
import tensorflow as tf
import keras_nlp

os.environ["KERAS_BACKEND"] = "tensorflow"

def generate_lore(prompt, temperature, model_path):
    """
    Loads the fine-tuned Chronicler model and generates a sequence based on the prompt.
    """
    if not os.path.exists(model_path):
        print(f"Error: Model weights not found at {model_path}. Please run train.py first.")
        return

    print("Awakening the Chronicler...")
    
    # Keras NLP generative models can easily load weights if the architecture is identical
    # However, since we used from_preset in train.py, we instantiate the exact same structure
    # and then load the weights.
    preprocessor = keras_nlp.models.GPT2CausalLMPreprocessor.from_preset(
        "gpt2_base_en",
        sequence_length=128
    )
    
    model = keras_nlp.models.GPT2CausalLM.from_preset(
        "gpt2_base_en",
        preprocessor=preprocessor
    )
    
    # Load fine-tuned weights
    try:
        model.load_weights(model_path)
    except Exception as e:
        print(f"Failed to load weights: {e}")
        return

    # Configure the generation sampler
    # Temperature scaling: 
    #   Low (< 0.5) = Rigid, historical records
    #   High (> 0.8) = Surrealism, cosmic dread parables
    sampler = keras_nlp.samplers.TopPSampler(p=0.9, temperature=temperature)
    model.compile(sampler=sampler)

    print("\n--- INCOMING TRANSMISSION ---\n")
    # Generate sequence
    output = model.generate(prompt, max_length=128)
    print(output)
    print("\n--- TRANSMISSION END ---\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query The Epoch Chronicler")
    parser.add_argument("--prompt", type=str, required=True, help="The seed phrase to initiate the lore generation")
    parser.add_argument("--temperature", type=float, default=0.8, help="Creativity/Surrealism control (e.g., 0.2 for rigid facts, 0.9 for cosmic dread)")
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_save_path = os.path.join(base_dir, "models", "epoch_chronicler.keras")
    
    generate_lore(prompt=args.prompt, temperature=args.temperature, model_path=model_save_path)
