import os
import openai

class ChatGPT:
    def getPrompt(self):
        return self.response["choices"][0]["text"].strip();

    def __init__(self, prompt = None):
        openai.api_key = "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"

        #self.prompt =  '영화 제목을 맞추는 퀴즈의 문제를 만들어보자. 내가 '+prompt+'이라고 말할 수 있도록 문제를 리스트로 만들어줘. 영화에 대한 추가 정보로 문제를 만들어야 해. 중요한 것은 내가 문제를 풀기 위해 답은 말하지 말아줘.'
        #self.prompt = "Let's create a movie quiz where I can say, 'The answer is " +prompt+ ".' Create a list of questions that lead to the answer with additional information about " +prompt+ ". Remember, don't explicitly mention the movie title in the questions to challenge me. Please provide the responses in Korean."
        self.prompt = "영화 줄거리를 기반으로 영화 제목을 유추하는 문제를 만들어보자. 다음은 영화의 줄거리야:\n\n" + prompt + "\n\n주목해야 할 점을 알려주는 힌트를 작성해줘."



        self.response = openai.Completion.create(
          model="text-davinci-003",
          prompt=self.prompt,
          temperature=0,    # 무작위성 제어, 높을 수록 텍스트가 다양하게 보일 수 있다
          max_tokens=3000 ,    # 높을 수록 단어가 많이 나오는 토큰 수
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )

if __name__ == "__main__":
    gpt = ChatGPT()
    print("=====================================")
    print(gpt.response["choices"][0]["text"].strip())
    print("=====================================")
