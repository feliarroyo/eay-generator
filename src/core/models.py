from operator import index
import os


VALID_LANGUAGES = ["en", "fr", "de", "es", "es-XL", "it"]
LANGUAGE_NAMES = ["English", "French", "German", "Español (España)", "Español (América Latina)", "Italian"]

EARWAX_CATEGORIES = ["household", "tools", "alarm", "vehicle", "Animal", "cartoon", "Music", "voice", "bodily functions", "sports", "liquid", "electronic/machine", "human", "crowd", "violence", "weather", "sexual", "sci-fi", "explosion"]

class EAYPrompt:
    def __init__(self, personal_question, screen_question, audio, suggestions, x, us):
        self.personal_question = personal_question
        self.screen_question = screen_question
        self.hasAudio = audio is not None
        self.audio = audio
        self.suggestions = suggestions
        self.x = x
        self.us = us

    def get_prompt_data(self):
        return {
            "personal_question": self.personal_question,
            "screen_question": self.screen_question,
            "hasAudio": self.hasAudio,
            "audio": self.audio if self.hasAudio else "",
            "suggestions": self.suggestions,
            "x": self.x,
            "us": self.us
        }
        
    def has_audio(self):
        return self.hasAudio

    def is_valid_prompt(self):
        if self.personal_question.strip() == "" or self.screen_question.strip() == "":
            return False
        if len(self.suggestions) < 1: # could need more, requires testing
            return False
        return True

class EarwaxSound:
    def __init__(self, name, short, x, category):
        self.name = name
        self.short = short
        self.x = x
        self.category = category

# EAY Custom Episode template:
class EAYCustomEpisode:
    def __init__(self, episode_name, prompts):
        self.episode_name = episode_name
        self.prompts = prompts

    def to_dict(self):
        return {
            "episodeName": self.episode_name,
            "prompts": [p.get_prompt_data() for p in self.prompts]
        }

# Fibbage 3 tmiShortie.jet:
class fib3EAYTemplate:
    def __init__(self, prompts):
        self.episodeid = 1309
        self.content = [
            {
                "x": prompt.x,
                "personal": prompt.personal_question,
                "id": index,
                "portrait": False,
                "category": "",
                "bumper": "",
                "us": prompt.us,
            }
            for index, prompt in enumerate(prompts)
        ]
    
    def to_dict(self):
        return {
            "episodeid": self.episodeid,
            "content": self.content
        }


# Fibbage 3 tmiShortie/<id>/data.jet:
class fib3EAYTemplate_Data:
    def __init__(self, prompt):
        self.fields = [
            {"t": "B", "v": "false", "n": "HasBumperAudio"},
            {"t": "B", "v": "false", "n": "HasKeywordAudio"},
            {"t": "B", "v": "false", "n": "HasBumperType"},
            {"t": "B", "v": "false", "n": "HasCorrectAudio"},
            {"t": "B", "v": "true", "n": "HasQuestionAudio"},
            {
                "t": "S",
                "v": ", ".join(prompt.suggestions[i] for i in range(len(prompt.suggestions))),
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
                "v": "questionAudio",
                "n": "QuestionAudio",
            },
        ]

    def to_dict(self):
        return {
            "fields": self.fields
        }


# Fibbage 4 eayBlankie.jet:
class fib4EAYTemplate:
    def adjust_formatting(self, text):
        # Replace <PLAYER> and <BLANK> with {{PLAYER}} and {{BLANK}}
        text = text.replace("<PLAYER>", "{{PLAYER}}").replace("<BLANK>", "{{BLANK}}")
        return text
    def __init__(self, prompts):
        self.content = [
            {
                "alternateSpellings": [],
                "bumper": "None",
                "category": "",
                "correctText": "",
                "extraCategories": [],
                "id": str(index),
                "isValid": "",
                "personal": self.adjust_formatting(prompt.personal_question),
                "portrait": False,
                "questionText": self.adjust_formatting(prompt.screen_question),
                "suggestions": prompt.suggestions,
                "us": prompt.us,
                "x": prompt.x,
            }
            for index, prompt in enumerate(prompts)
        ]
    def to_dict(self):
        return {
            "content": self.content
        }


# Fibbage 4 eayBlankie/<id>/data.jet:
class fib4EAYTemplate_Data:
    def adjust_formatting(self, text):
            # Replace <PLAYER> and <BLANK> with {{PLAYER}} and {{BLANK}}
            text = text.replace("<PLAYER>", "{{PLAYER}}").replace("<BLANK>", "{{BLANK}}")
            return text
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
                "s": self.adjust_formatting(prompt.screen_question),
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

    def to_dict(self):
        return {
            "fields": self.fields
        }