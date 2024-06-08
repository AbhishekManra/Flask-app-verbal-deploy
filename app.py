import pathlib
import textwrap

import google.generativeai as genai

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Replace with your actual API key
genai.configure(api_key="AIzaSyCfdxk1c4hbTiqr-0OL4M8Y0STgOGVXmYk")
# genai.configure(api_key="AIzaSyCpNiz9zXnzI2XkL8U26xH0-VMwH9mg9ig")

model = genai.GenerativeModel('gemini-1.5-flash')

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

@app.route('/generate', methods=['POST'])
def generate_content():
    if request.content_type == 'application/json':
        # data = request.json
        data = request.get_json()
        # print(data)
        # data = request.json.get('data')
        # print(data.messages[0])
        messages = data.get('messages', []) 
        # messages = data.messages[0] 
        conversation = '\n'.join([f"{msg['sender']}: {msg['content']}" for msg in messages])
        # print(conversation)
        prompt = f"{conversation}\n\nThis is the conversation between me and a Person on Bumble (dating site). Looking at the conversation, generate a message on behalf of me ,my name is Abhishek, just give a response from my side nothing extra.\n "
        print(prompt)
        response = model.generate_content(prompt)
        # result = response.candidates[0].content.parts[0].text
        try: # make a statement that changes the api
            result = response.candidates[0].content.parts[0].text
            print(result)
            # result = "sucess"
        except IndexError:
            return "Error retrieving response from API.", 500
        # result = response.candidates[0].content.parts[0].text
        print("This is the result")
        print(result)
        return jsonify({'result': result})
    else:
        return 'Unsupported Media Type', 415

if __name__ == '__main__':
    app.run(debug=True)