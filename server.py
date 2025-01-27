from flask import Flask, render_template
import datetime
import git_scraper

app = Flask(__name__)


@app.route('/')
def hello_world():
    data = git_scraper.get_commit_data()
    git_scraper.create_df(data)
    for_footer_datetime = datetime.date.today().year
    graph_ = git_scraper.create_graph('data.csv')
    return render_template('index.html', footer_data=for_footer_datetime, table_graph=graph_)


if __name__ == '__main__':
    app.run(debug=True)
