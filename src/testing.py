import json

class Episode:
    def __init__(self, episode_name):
        self.episode_name = episode_name  # string
        self.prompts = []  # list of Prompt objects
    
    def addPromptToEpisode(self, prompt):
        """Adds a Prompt object to the episode's prompts list."""
        self.prompts.append(prompt)
        
    def getPrompts(self):
        """Returns the list of prompts in the episode."""
        return self.prompts
    
    def editPrompt(self, prompt_id, new_prompt):
        """Edits an existing prompt in the episode."""
        for i, prompt in enumerate(self.prompts):
            if prompt.prompt_id == prompt_id:
                self.prompts[i] = new_prompt
                return True
        return False  # Return False if the prompt was not found
    
    def removePrompt(self, prompt_id):
        """Removes a prompt from the episode based on its ID."""
        for i, prompt in enumerate(self.prompts):
            if prompt.prompt_id == prompt_id:
                del self.prompts[i]
                return True
        return False  # Return False if the prompt was not found

class Prompt:
    def __init__(self, prompt_id, personal_question, screen_question, suggestions, x, us):
        self.prompt_id = prompt_id # number for now (check if strings allowed)
        self.personal_question = personal_question # string
        self.screen_question = screen_question # string
        self.suggestions = suggestions # array of strings
        self.x = x  # boolean
        self.us = us # boolean
    
    def getPersonalQuestion(self):
        """Returns the personal question of the prompt."""
        return self.personal_question
    
    def getScreenQuestion(self):
        """Returns the screen question of the prompt."""
        return self.screen_question
    
    def getSuggestions(self):
        """Returns the suggestions of the prompt."""
        return self.suggestions
    
# Episode variables
episodeName = "Episodio"
episode = Episode(episodeName)

# Prompt variables
promptId = 0  # Make getId function later
personalQuestion = "Pregunta en el celular"
screenQuestion = "Pregunta para la pantalla"
suggestions = ["Sugerencia 1", "Sugerencia 2", "Sugerencia 3"]
x = False  # True or False
us = False  # True or False
prompt = Prompt(promptId, personalQuestion, screenQuestion, suggestions, x, us)
episode.addPromptToEpisode(prompt)

# Fibbage 3 tmiShortie.jet:
fib3Template = {
    "episodeid": 1309,
    "content": [
        {
            "x": x,
            "personal": personalQuestion,
            "id": promptId,
            "portrait": False,
            "category": "",
            "bumper": "",
            "us": us,
        }
    ],
}

# Fibbage 3 tmiShortie/<id>/data.jet:
fib3DataTemplate = {
    "fields": [
        {"t": "B", "v": "false", "n": "HasBumperAudio"},
        {"t": "B", "v": "false", "n": "HasKeywordAudio"},
        {"t": "B", "v": "false", "n": "HasBumperType"},
        {"t": "B", "v": "false", "n": "HasCorrectAudio"},
        {"t": "B", "v": "true", "n": "HasQuestionAudio"},
        {
            "t": "S",
            "v": suggestions,
            "n": "Suggestions",
        },
        {
            "t": "S",
            "v": personalQuestion,
            "n": "PersonalQuestionText",
        },
        {"t": "S", "v": "", "n": "Category"},
        {"t": "S", "v": "", "n": "CorrectText"},
        {"t": "S", "v": "None", "n": "BumperType"},
        {
            "t": "S",
            "v": screenQuestion,
            "n": "QuestionText",
        },
        {"t": "S", "v": "", "n": "SocialMediaDate"},
        {"t": "S", "v": "", "n": "KeywordResponse"},
        {"t": "S", "v": "", "n": "SocialMediaName"},
        {"t": "S", "v": "", "n": "AlternateSpellings"},
        {
            "s": "",
            "t": "A",
            "n": "KeywordResponseAudio",
        },
        {"s": "[category=host]", "t": "A", "n": "BumperAudio"},
        {"t": "G", "n": "Pic"},
        {"s": "[category=host]", "t": "A", "n": "CorrectAudio"},
        {
            "s": "screenQuestion",
            "t": "A",
            "v": "questionAudio",
            "n": "QuestionAudio",
        },
    ]
}

# Fibbage 4 eayBlankie.jet:
fib4Template = {
    "content": [
        {
            "alternateSpellings": [],
            "bumper": "None",
            "category": "",
            "correctText": "",
            "extraCategories": [],
            "id": promptId,
            "isValid": "",
            "personal": personalQuestion,
            "portrait": False,
            "questionText": screenQuestion,
            "suggestions": suggestions,
            "us": us,
            "x": x,
        }
    ]
}

# Fibbage 4 eayBlankie/<id>/data.jet:
fib4DataTemplate = {
    "fields": [
        {"t": "B", "v": "false", "n": "HasBumperAudio"},
        {"t": "B", "v": "false", "n": "HasKeywordAudio"},
        {"t": "B", "v": "false", "n": "HasCorrectAudio"},
        {"t": "B", "v": "true", "n": "HasQuestionAudio"},
        {"t": "A", "v": "bumperAudio", "n": "BumperAudio"},
        {"t": "A", "v": "correctAnswer", "n": "CorrectAudio"},
        {"t": "A", "v": "questionAudio", "n": "QuestionAudio", "s": screenQuestion},
        {"t": "B", "v": "false", "n": "HasPic"},
        {"t": "G", "v": "picture", "n": "Pic"},
        {"t": "B", "v": "false", "n": "HasSetupVideo"},
        {"t": "", "v": "setupVideo", "n": "SetupVideo"},
        {"t": "B", "v": "false", "n": "HasSetupAudio"},
        {"t": "A", "v": "setupAudio", "n": "SetupAudio"},
        {"t": "B", "v": "false", "n": "HasFeaturedStill"},
        {"t": "G", "v": "featuredStill", "n": "FeaturedStill"},
        {"t": "B", "v": "false", "n": "HasTransitionStill"},
        {"t": "G", "v": "transitionStill", "n": "TransitionStill"},
        {"t": "B", "v": "false", "n": "HasSetupSubtitles"},
        {"t": "", "v": "setupSubtitles", "n": "SetupSubtitles"},
        {"t": "B", "v": "false", "n": "HasRevealVideo"},
        {"t": "", "v": "revealVideo", "n": "RevealVideo"},
        {"t": "B", "v": "false", "n": "HasRevealAudio"},
        {"t": "A", "v": "revealAudio", "n": "RevealAudio"},
        {"t": "B", "v": "false", "n": "HasRevealSubtitles"},
        {"t": "", "v": "revealSubtitles", "n": "RevealSubtitles"},
    ]
}

test = fib3Template

# the result is a JSON string:
print(json.dumps(test))

# convert into JSON:
with open('data.json', 'w', encoding='utf-8') as f:
    templateToJson = json.dump(test, f, ensure_ascii=False, indent=4)
    
def getId():
    """Function to get the prompt ID."""
    global promptId
    promptId += 1
    return promptId

def addPrompt():
    """Function to add a new prompt."""
    global personalQuestion, screenQuestion, suggestions, x, us
    # Logic to add a new prompt goes here
    # For example, you could update the variables based on user input
    pass