import re,json
from nltk.stem import WordNetLemmatizer
from os import system

def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("botResponse.json")

def splitAndStem(userInput: str) -> list[str]:
    wordLemmatizer = WordNetLemmatizer()
    split_message= re.split( r'\s+|[,;?!.-]\s*', userInput.lower() ) 
    stemmed = [wordLemmatizer.lemmatize(word) for word in split_message if word != '']
    print(stemmed)
    return stemmed

    
def instruction_mode():
    
    print("Ativated instruction mode")
    
def get_responce(userInput):
    
    splitUserInput : list= splitAndStem(userInput= userInput)
    score_list : list[int]= [] 

    for response in response_data:
        
        responseScore = 0
        requiredScore = 0
        requiredWords = response['required_words']
        
        if  requiredWords:
 
            
            for word in splitUserInput:
                if word in requiredWords:
                    requiredScore += 1
                    
        if requiredScore == len(requiredWords):
            for word in splitUserInput:
                if word in response['user_input']:
                    responseScore += 1
                    
        score_list.append(responseScore)
     
    bestres = max(score_list)
    responseIndex = score_list.index(bestres)
    
    if userInput == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if bestres != 0:
        print(response_data[responseIndex]["response_type"])
        return response_data[responseIndex]["bot_response"]





# main function     
def main() -> None:
    
    while True:
        print("_________________")
        userInput = input("User: ")
        if userInput.lower() == 'exit':
            break
        elif userInput == 'clear':
            system('cls')
        else:
            print(f'assistant: {get_responce(userInput= userInput)}' )
        
        
        
        
    
    
if __name__ == '__main__':
    main()