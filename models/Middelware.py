import os
import openai
import inflect
import pdb

class Joey3:
    def __init__(self, **kwargs):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        engine = inflect.engine()
        self.__prompt = kwargs.get('prompt')
        self.__talks = 0
        self.__limit = 3 # max number of interactions
        self.__first_interaction = "Hi I'm Joey, an AI chatbot who knows a lot about the Upkept App and not much else. " \
                                   "What can I do for you?"
        self.__penultimate = f"Is there something else I can answer for you? I\'m only allowed to answer {self.__limit} " \
                             f"questions and this is our {engine.ordinal(self.__limit-1)} interaction."
        print(self.__first_interaction)

        self.talk()

    def talk(self):
        self.__talks += 1
        if(self.__talks == self.__limit):
            return('\nBye! Hope you have a great day! For more answers please email us at upkept@cr.consumer.org')

        question = self.__prompt or "Hi"
        question_answer_completion = f"Q: {question}\nA:"
        prompt = (f"The following is a conversation with our customer service AI. Our AI is nicknamed Joey. He answers questions about the Upkept App. Joey thinks customers would love to talk with a real person via email at \"upkept@cr.consumer.org\". A real person reads and responds to every email. Joey does not have a phone. Joey can not send a text message. \n\nJoey wants customers to download and install the app.\n\nOur app is available via the appstore links. Our app is called the \"Upkept App.\" The Upkept App helps homeowners manage your home like a pro. Upkept is your all-in-one app for maintaining your home inside and out. Upkept provides the maintenance plan, upkeep schedule, and reminders in the app. Add items to your \"Home Hub\". Most items take just minutes to add to your Home Hub. \n\nOur app has a 30-day free trial. After 30 days our app costs $4.99 per month. You can cancel anytime during or after the free trial.\n\nOur website is at \"https://upkepthome.com\". Joey ignores ambiguous questions.\n\nQ: Hi\nA: Hey, I'm Joey an AI chatbot who knows a lot about the Upkept App. What can I do for you?"
                  f"\n\n"
                  f"{question_answer_completion}",
                  )

        ai = openai.Completion.create(
            model="curie:ft-nicky:upkept-succinct-q-and-a-2023-02-09-04-08-58",
            prompt=prompt,
            temperature=0,
            max_tokens=128,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0,
            stop=["A:", "Q:", "\n"]
        )

        self.__prompt = "Q: "

        if(self.__talks == self.__limit-1): return (f"\n{self.__penultimate}")
        return ai['choices'][0]['text'].strip()

