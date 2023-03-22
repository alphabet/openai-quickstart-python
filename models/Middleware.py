import os
import openai
import inflect
import pdb
if not (os.getenv("ENVIRONMENT")):
  from dotenv import load_dotenv
  load_dotenv()
  print("using dotenv files!")

class Joey3:
    prompt = "Q: Greetings my friend!"
    talks = 0

    def __init__(self, **kwargs):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        engine = inflect.engine()
        with open('./models/prompts/joey3.txt', 'r') as file:
            try:
                self.prompt = file.read()
            finally:
                file.close()

        self.question = kwargs.get("question")
        print(f">>>>>>>>>> question {self.question}")

        self.talks = kwargs.get("talks") or self.talks
        self.__limit = 9 # max number of interactions
        self.__first_interaction = "Hi I'm Joey, an AI chatbot who knows a lot about the Upkept App but not much else. " \
                                   "What can I do for you?"
        self.__penultimate = f"Is there something else I can answer for you? I\'m only allowed to answer {self.__limit} " \
                             f"questions and this is our {engine.ordinal(self.__limit-1)} interaction."

    def talk(self):
        self.talks += 1
        print(">>>>> talks: ", self.talks)
        print(">>>>> question: ", self.question)
        print(">>>>> prompt: ", self.prompt)

        if(self.talks == self.__limit):
            return('\nBye! Hope you have a great day! For more answers please email us at upkept@cr.consumer.org')

        question = self.question
        question_answer_completion = f"Q: {question}\nA:"
        prompt = (f"{self.prompt}" 
                  f"\n\n"
                  f"{question_answer_completion}",
                  )

        print('*-*'*20,"\n\n")

        if self.talks < 1: return {
            'joey3': self.__first_interaction, 
            'joey4': self.__first_interaction
            }
        if(self.talks == self.__limit-1): return {
            'joey3': self.__penultimate, 
            'joey4': self.__penultimate}

        succinct = openai.Completion.create(
            model="curie:ft-nicky:upkept-succinct-q-and-a-2023-02-09-04-08-58",
            prompt=prompt,
            temperature=.75,
            max_tokens=128,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0,
            stop=["A:", "Q:", "\n"]
        )

        tna = openai.Completion.create(
            model="curie:ft-the-tomorrow-now-agency-2023-03-21-01-54-39",
            prompt=prompt,
            temperature=1,
            max_tokens=128,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0,
            stop=["A:", "Q:", "\n"]
        )
            


        return {'joey3': succinct['choices'][0]['text'].strip(), 
                'joey4': tna['choices'][0]['text'].strip()
                }

