from nltk.stem import PorterStemmer
import json, re

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("botResponse.json")

class Chatbot:
        
    def __init__(self) -> None:
        self.memory : list[dict] = []
        # self.responseData = json.load("../basicChatBot/botResponse.json")
        
        
    def get_responce(self, user_input):
        porter_stemmer = PorterStemmer()
        split_message= re.split( r'\s+|[,;?!.-]\s*', user_input.lower() ) 
        stemmed_words = [porter_stemmer.stem(word) for word in split_message]
        
        return stemmed_words    



def main() -> None:
    
    chat_bot = Chatbot()
    
    while True:
        chat = input('User: ')
        if chat == 'exit':
            break
        print(f'User chat: {chat}')
        print(f'responce: {chat_bot.get_responce(chat)}')


if __name__ == '__main__':
    
    main()