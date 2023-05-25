import os
import openai

class ChatGPT:
    def getPrompt(self):
        return self.response["choices"][0]["text"].strip();

    def __init__(self, prompt = None):
        openai.api_key = "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"

        if prompt is None:
            self.prompt = input("지시사항을 입력하세요: ")
        else:
            self.prompt = prompt+' 의 줄거리를 요약해줘'

        self.response = openai.Completion.create(
          model="text-davinci-003",
          prompt=self.prompt,
          temperature=1,    # 무작위성 제어, 높을 수록 텍스트가 다양하게 보일 수 있다
          max_tokens=4000 ,    # 높을 수록 단어가 많이 나오는 토큰 수
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )

if __name__ == "__main__":
    gpt = ChatGPT()
    print("=====================================")
    print(gpt.response["choices"][0]["text"].strip())
    print("=====================================")
