from flask import Flask, render_template, request,flash,redirect
import openai

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

# 设置你的ChatGPT API密钥
api_key = "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"



@app.route('/', methods=['GET','POST'])
def ask():
    if request.method == 'POST':
        user_input = request.form.get('question')
        flash(user_input)
        if user_input:
            flash('Normal Situation')
        # 调用ChatGPT API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=50,
            api_key=api_key
        )

        answer = response.choices[0].text.strip()

        return render_template('index.html', question=user_input, answer=answer)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
