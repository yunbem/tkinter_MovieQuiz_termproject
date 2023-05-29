import os
import openai

class ChatGPT:
    def getPrompt(self):
        return self.response["choices"][0]["text"].strip();

    def __init__(self, prompt = None):
        openai.api_key = "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"

        self.prompt = '영화 제목을 맞추는 퀴즈의 문제를 만들어보자. 영화 제목의 정답은 영화 '+prompt+' 이야. 무조건 정답인 영화 제목을 숨겨야 해.네가 문제를 내봐.'
        self.response = openai.Completion.create(
          model="text-davinci-003",
          prompt=self.prompt,
          temperature=1,    # 무작위성 제어, 높을 수록 텍스트가 다양하게 보일 수 있다
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
