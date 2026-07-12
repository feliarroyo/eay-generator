class Prompt:
    def __init__(self, personal_question, screen_question, audio, suggestions, x, us):
        self.personal_question = personal_question
        self.screen_question = screen_question
        self.hasAudio = audio != "(No audio)"
        self.audio = audio
        self.suggestions = suggestions
        self.x = x
        self.us = us

    def get_prompt_data(self):
        return {
            "personalQuestion": self.personal_question,
            "screenQuestion": self.screen_question,
            "hasAudio": self.hasAudio,
            "audio": self.audio,
            "suggestions": self.suggestions,
            "x": self.x,
            "us": self.us
        }
        
    def has_audio(self):
        return self.hasAudio

# Fibbage 3 tmiShortie.jet:
class fib3Template:
    def __init__(self, prompts):
        self.episodeid = 1309
        self.content = [
            {
                "x": prompt.x,
                "personal": prompt.personal_question,
                "id": prompt.prompt_id,
                "portrait": False,
                "category": "",
                "bumper": "",
                "us": prompt.us,
            }
            for prompt in prompts
        ]


# Fibbage 3 tmiShortie/<id>/data.jet:
class fib3Template_Data:
    def __init__(self, prompt):
        self.fields = [
            {"t": "B", "v": "false", "n": "HasBumperAudio"},
            {"t": "B", "v": "false", "n": "HasKeywordAudio"},
            {"t": "B", "v": "false", "n": "HasBumperType"},
            {"t": "B", "v": "false", "n": "HasCorrectAudio"},
            {"t": "B", "v": "true", "n": "HasQuestionAudio"},
            {
                "t": "S",
                "v": prompt.suggestions,
                "n": "Suggestions",
            },
            {
                "t": "S",
                "v": prompt.personal_question,
                "n": "PersonalQuestionText",
            },
            {"t": "S", "v": "", "n": "Category"},
            {"t": "S", "v": "", "n": "CorrectText"},
            {"t": "S", "v": "", "n": "BumperType"},
            {
                "t": "S",
                "v": prompt.screen_question,
                "n": "QuestionText",
            },
            {"t": "", "v": "", "n": "SocialMediaDate"},
            {"t": "", "v": "", "n": "KeywordResponse"},
            {"t": "", "v": "", "n": "SocialMediaName"},
            {"t": "", "v": "", "n": "AlternateSpellings"},
            {"s": "", "t": "A", "n": "KeywordResponseAudio"},
            {"s": "[category=host]", "t": "A", "n": "BumperAudio"},
            {"t": "G", "n": "Pic"},
            {"s": "[category=host]", "t": "A", "n": "CorrectAudio"},
            {
                "s": prompt.screen_question,
                "t": "A",
                "v": prompt.audio,
                "n": "QuestionAudio",
            },
        ]


# Fibbage 4 eayBlankie.jet:
class fib4Template:
    def __init__(self, prompts):
        self.content = [
            {
                "alternateSpellings": [],
                "bumper": "None",
                "category": "",
                "correctText": "",
                "extraCategories": [],
                "id": prompt.prompt_id,
                "isValid": "",
                "personal": prompt.personal_question,
                "portrait": False,
                "questionText": prompt.screen_question,
                "suggestions": prompt.suggestions,
                "us": prompt.us,
                "x": prompt.x,
            }
            for prompt in prompts
        ]


# Fibbage 4 eayBlankie/<id>/data.jet:
class fib4Template_Data:
    def __init__(self, prompt):
        self.fields = [
            {"t": "B", "v": "false", "n": "HasBumperAudio"},
            {"t": "B", "v": "false", "n": "HasKeywordAudio"},
            {"t": "B", "v": "false", "n": "HasCorrectAudio"},
            {"t": "B", "v": "true", "n": "HasQuestionAudio"},
            {"t": "A", "v": "bumperAudio", "n": "BumperAudio"},
            {"t": "A", "v": "correctAnswer", "n": "CorrectAudio"},
            {
                "t": "A",
                "v": "questionAudio",
                "n": "QuestionAudio",
                "s": prompt.screenQuestion,
            },
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
