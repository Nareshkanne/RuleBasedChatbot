import re
import random
import spacy

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Open log file in append mode to store the conversation
log_file = open("chatlog.txt", "a")

# Initialize user data dictionary
user_data = {}

# Function to handle greetings
def handle_greeting(user_input):
    if re.search(r'\b(hello|hi|hey)\b', user_input):
        responses = ["Hello! How can I help you?", "Hi there!", "Hey! What's up?"]
        return random.choice(responses)
    return None

# Function to handle name query and store user's name
def remember_name(user_input, user_data):
    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip()
        user_data["name"] = name
        return f"Got it! I'll remember your name, {name}."
    elif "what's my name" in user_input and "name" in user_data:
        return f"Your name is {user_data['name']}."
    return None

# Function to handle jokes
def handle_joke(user_input):
    if re.search(r'\bjoke\b', user_input):
        jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don’t have the guts!",
            "What do you call cheese that isn't yours? Nacho cheese!"
        ]
        return random.choice(jokes)
    return None

# Function to handle the help command
def handle_help(user_input):
    if user_input == "help":
        return (
            "You can ask me things like:\n"
            "- Hello\n"
            "- What is your name?\n"
            "- Tell me a joke\n"
            "- What's my name?\n"
            "- Type 'bye' or 'exit' to leave the chat"
        )
    return None

# Function to analyze user input using spaCy (NLP)
def analyze_sentence(user_input):
    doc = nlp(user_input)
    analysis = []
    for token in doc:
        analysis.append(f"{token.text} ({token.pos_})")  # Word and its part of speech
    return " ".join(analysis)

# Function to log the conversation
def log_conversation(user_input, response):
    log_file.write(f"You: {user_input}\nChatbot: {response}\n\n")

# Main chatbot function
def chatbot():
    print("Chatbot: Hi! I'm here to chat with you. Type 'help' for options or 'bye' to exit.")
    while True:
        # Get user input
        user_input = input("You: ").strip().lower()

        # Check if input is empty
        if not user_input:
            response = "Please say something!"
            print(f"Chatbot: {response}")
            log_conversation(user_input, response)
            continue

        # Rule-based responses using functions
        response = handle_greeting(user_input) or \
                   remember_name(user_input, user_data) or \
                   handle_joke(user_input) or \
                   handle_help(user_input)

        # If no match found, default response
        if response is None:
            if user_input in ["bye", "exit"]:
                response = "Goodbye! Take care!"
                print(f"Chatbot: {response}")
                log_conversation(user_input, response)
                break
            else:
                # Analyze user input with NLP
                nlp_response = analyze_sentence(user_input)
                response = f"I analyzed your sentence: {nlp_response}"

        print(f"Chatbot: {response}")
        log_conversation(user_input, response)

# Start the chatbot
if __name__ == "__main__":
    chatbot()

# Close the log file when exiting
log_file.close()
