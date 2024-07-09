
from hugchat import hugchat
from hugchat.login import Login
from random import randint


class HugchatAgent:
    CookiePath = './cookies/'

    def __init__(self, email: str, password: str) -> None:
        self.email = email

        self.auth = Login(self.email, password)
        self.cookies = self.auth.login(cookie_dir_path=HugchatAgent.CookiePath, save_cookies=True)

        self.chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict())

        self.active_model: hugchat.Model | None = None

    def activate(self, pattern_prompt: str):
        '''Select your llm model (random for now), and set your start prompt, which all the prompt comming later will be processed based on this prompt.'''
        models = self.chatbot.get_available_llm_models()
        active_model_index = randint(0, len(models) - 1)
        self.chatbot.switch_llm(active_model_index)
        self.active_model = self.chatbot.active_model
        return self.prompt(pattern_prompt)


    def prompt(self, prompt: str, web_search: bool = False):
        return self.chatbot.query(prompt, web_search=web_search)