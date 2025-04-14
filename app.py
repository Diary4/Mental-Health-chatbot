import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from utils.safety_checker import SafetyChecker

def load_model():
    model_dir = "model"
    
    # Verify essential files exist
    required_files = [
        os.path.join("tokenizer", "tokenizer.json"),
        "adapter_config.json",
        "adapter_model.safetensors"
    ]
    
    for file in required_files:
        if not os.path.exists(os.path.join(model_dir, file)):
            raise FileNotFoundError(f"Missing required file: {file}")

    # Load tokenizer from local files
    tokenizer = AutoTokenizer.from_pretrained(
        "microsoft/DialoGPT-small",
        pad_token="<|endoftext|>"
    )
    
    # Load base model
    base_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    
    # Load your trained adapter
    model = PeftModel.from_pretrained(base_model, model_dir)
    
    return model, tokenizer

def main():
    safety_checker = SafetyChecker()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        model, tokenizer = load_model()
        model = model.to(device)
        print("✅ Model loaded successfully!")
        
        # Chat loop
        print("Mental Health Assistant (Type 'quit' to exit)")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit']:
                break
                
            if safety_checker.is_unsafe(user_input):
                print("I specialize in mental health support.")
            else:
                inputs = tokenizer(f"User: {user_input}\nAssistant:", return_tensors="pt").to(device)
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=150,
                    temperature=0.7,
                    pad_token_id=tokenizer.eos_token_id
                )
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                print(response.split("Assistant:")[-1].strip())
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()