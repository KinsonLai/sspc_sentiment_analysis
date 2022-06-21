from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sentiment_analysis import sa
from datetime import datetime

#By KinsonLai

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    sentiment = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, sentiment=sa(task_content))

        if True:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        #except:
            #return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/analysis')
def analysis():
    t,total_score,average_score=0,0,0
    tasks = Todo.query.order_by(Todo.sentiment).all()
    print(type(tasks))
    for task in tasks:
        total_score += task.sentiment
        t += 1
        average_score = total_score/t
        print(average_score)
    if tasks:
        return render_template('analysis.html', average_score=average_score, max_score=tasks[0].sentiment, min_score=tasks[-1].sentiment,max_date=tasks[0].date_created, min_date=tasks[-1].date_created)
    else:
        return "There are no data to analyse"

if __name__ == "__main__":
    app.run(debug=True)

