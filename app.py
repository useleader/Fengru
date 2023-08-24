from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# 在这里填入你的OpenAI API密钥
openai.api_key = "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"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]

    # 调用ChatGPT API进行对话
    response = openai.Completion.create(
        engine="davinci-codex",  # 或者你想使用的其他GPT-3引擎
        prompt=user_input,
        max_tokens=50,  # 控制生成文本的长度
    )

    chat_response = response.choices[0].text.strip()
    return render_template(
        "index.html", user_input=user_input, chat_response=chat_response
    )


if __name__ == "__main__":
    app.run(debug=True)
