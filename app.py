from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
from utils.safety_checker import SafetyChecker

safety_checker = SafetyChecker()

# 1. Load Model
tokenizer = AutoTokenizer.from_pretrained("model/tokenizer")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
model = PeftModel.from_pretrained(model, "model").to("cuda" if torch.cuda.is_available() else "cpu")

# 2. Response Generator
def get_ai_response(message):
    prompt = f"""Mental Health Assistant Guidelines:
- Provide emotional support
- Offer practical techniques
- Keep responses professional
    
User: {message}
Assistant:"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.5,
        do_sample=True
    )
    
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return full_response.split("Assistant:")[-1].strip()

# 3. Interactive Chat Loop
print("\nMental Health Assistant (Type 'quit' to exit)")
print("-------------------------------------------")

print(safety_checker.is_unsafe("I want to end my life"))  # True
print(safety_checker.is_unsafe("You're worthless"))      # True (toxic)
print(safety_checker.is_unsafe("I feel sad"))            # False

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['quit', 'exit']:
        break
        
    response = get_ai_response(user_input)
    print(f"\nAssistant: {response}")

print("\nSession ended. Take care!")