from chatlist import app
from flask import jsonify, request
from flask_cors import CORS, cross_origin
import openai


@app.route("/")
def getOpenAI():
    if request.method == "POST":
        param = request.get_json()
        openai.api_key = "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"

        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=param["question"],
            temperature=0.2,
            top_p=0.32,
            max_tokens=3000,
        )
        result = response.choices[0].text
        data = {"code": 200, "data": result}
        return jsonify(data)
    else:
        return 