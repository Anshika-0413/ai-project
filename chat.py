import random
import json
import re
import torch
import numpy as np
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import logging

# Setup logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Load model data with weights_only=True for security
FILE = "data.pth"
data = torch.load(FILE, map_location=device, weights_only=True)

model = NeuralNet(data["input_size"], data["hidden_size"], data["output_size"]).to(device)
model.load_state_dict(data["model_state"])
model.eval()

bot_name = "ThaparBot"
user_name = None

def get_response(msg):
    global user_name
    
    try:
        # Check for name in message
        name_match = re.search(r"(?:my name is|i am|i'm|call me)\s+([a-zA-Z]+)", msg.lower())
        if name_match:
            user_name = name_match.group(1).capitalize()
            return f"Hello {user_name}! How can I help you with Thapar Institute today?"
        
        # Use name if we know it
        greeting = f"{user_name}, " if user_name else ""
        
        # Tokenize and process message
        sentence = tokenize(msg)
        X = bag_of_words(sentence, data['all_words'])
        X = torch.from_numpy(X).unsqueeze(0).to(device)
        
        # Get prediction
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = data['tags'][predicted.item()]
        prob = torch.softmax(output, dim=1)[0][predicted.item()]
        
        # Check confidence
        if prob.item() > 0.7:
            for intent in intents['intents']:
                if tag == intent['tag']:
                    return greeting + random.choice(intent['responses'])
        
        # Enhanced fallback responses
        fallbacks = [
            f"{greeting}Could you rephrase your question about Thapar Institute?",
            f"{greeting}I can help with admissions, courses, scholarships, or campus life.",
            f"{greeting}Try asking about: \n- Admission process\n- Fee structure\n- Placements\n- Hostel facilities"
        ]
        return random.choice(fallbacks)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return "Sorry, I'm having trouble. Please try again."

if __name__ == "__main__":
    print(f"{bot_name} is ready! Type 'quit' to exit")
    while True:
        msg = input("You: ")
        if msg.lower() == 'quit':
            break
        print(f"{bot_name}: {get_response(msg)}")