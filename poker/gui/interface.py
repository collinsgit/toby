from flask import Flask, render_template
app = Flask(__name__,
            static_folder='react-app/build/static',
            template_folder='react-app/build')


@app.route("/")
def user_interface():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
