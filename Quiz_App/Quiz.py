from re import S
from token import NUMBER
import requests
import re 

# Removing html elements from the api
pattern = re.compile(r'<[^>]+>')
NUMBER_QUESTIONS = 10;
class HTML_Remover:
    @staticmethod
    def remove_html_elements_from_list(li):
        clean_li = []
        for item in li:
            clean_li.append(re.sub(pattern, '', item.replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", ";")))
        
        return clean_li    

# Main quiz class
class Quizzer:
    
    # Initialise with optional difficulty and category
    def __init__(self, difficulty="any difficulty", category=0):    
   
        # API request set up
        ENDPOINT = "https://opentdb.com/api.php"
        PARAMS = {
            "amount" : 10,
            "type" : "multiple",
            }
        if category > 0:
            PARAMS["category"] = category
        if difficulty != "any difficulty":
            PARAMS["difficulty"] = difficulty
        
        # Request
        data = requests.get(url=ENDPOINT, params=PARAMS).json()

        invalid = True  
        while invalid:
            try:
                # Set up the class attributes
                self.question = [re.sub(pattern, '', data["results"][x]["question"]).replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", ";") for x in range(NUMBER_QUESTIONS)]
                self.correct_answer = [re.sub(pattern, '', data["results"][x]["correct_answer"]).replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", ";") for x in range(NUMBER_QUESTIONS)]
                self.wrong_answers = [HTML_Remover().remove_html_elements_from_list(data["results"][x]["incorrect_answers"]) for x in range(NUMBER_QUESTIONS)]
                invalid = False
            except:
                data = requests.get(url=ENDPOINT, params=PARAMS).json()
                
            
        