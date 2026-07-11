class Prompt:
    def __init__(self, personal_question, screen_question, audio,suggestions, x, us):
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