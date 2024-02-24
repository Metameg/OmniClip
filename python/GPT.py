from openai import OpenAI
import os
from dotenv import load_dotenv

class QuoteGenerator():
	def __init__(self, msg):
		load_dotenv()
		api_key = os.getenv('OPENAI_API_KEY')
		self.client = OpenAI(api_key=api_key)
		self.content = msg

	def generate(self):

		response = self.client.chat.completions.create(
			model="gpt-3.5-turbo",
			# max_tokens=20,
			messages=[
				{"role": "system", "content": "You work in digital marketing. You need to create a catchy, feel-good, one-liner quote that will act as a promotional sentence for a video your company has created. The guidelines of the quote will be given to you by the user."},
				{"role": "system", "content": "This quote should not have quotation marks in it. The "" characters should never be included in your response."},

				{"role": "user", "content": f'Here are your guidelines for this video: {self.content}.\n Create a short opening sentence that is no longer than 20 words for this promotional video.'},
			]
		)

		print("prompt_tokens: ", response.usage.prompt_tokens)
		print("completion_tokens: ", response.usage.completion_tokens)
		print("total_tokens: ", response.usage.total_tokens)

		return response.choices[0].message.content

if __name__ == '__main__':
	msg = '''I want a quote that engages a millenial audience and shows off money and a luxury lifestyle.'''
	gpt = QuoteGenerator( msg )
	response = gpt.generate()
	print(response)



