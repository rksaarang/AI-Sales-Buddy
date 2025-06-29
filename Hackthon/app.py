from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import openai
import json
from newsapi import NewsApiClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales_diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
jwt = JWTManager(app)
CORS(app)

# === OpenAI API Key ===
openai.api_key = 'Enter you key'
# === NewsAPI Setup ===
#newsapi = NewsApiClient(api_key='95d2a67099f04d5f95a59945cc32d9ca')

# === Models ===
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    sales_estimated = db.Column(db.Float, nullable=True)
    proposal_given = db.Column(db.Boolean, default=False)
    sector = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    sentiment = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === Sentiment Analysis Function ===
def analyze_sentiment(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis assistant."},
                {"role": "user", "content": f"Classify the sentiment of this sales note as Positive, Neutral, or Negative:\n\n{text}"}
            ],
            temperature=0,
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Sentiment error: {e}")
        return "Unknown"

# === Company Insights Function ===
def get_company_insights(company_name):
    prompt = f"""
You are a Business Research Analyst.

Give me a JSON with:
- title
- latest_developments (list)
- market_position (short paragraph)
- competitors (list)
- trends (list)
- opportunities (list)
- challenges (list)
- future_outlook (one of Growth, Stagnation, Decline with 1 line reason)

Company: {company_name}

Reply strictly in JSON.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a business research assistant. Reply in JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"Company Insights Error: {e}")
        return {"error": "AI service failed."}

# === Market News Function ===
def fetch_market_news():
    try:
        top_headlines = newsapi.get_top_headlines(
            category='business',
            language='en',
            country='us'
        )
        news_list = []
        for article in top_headlines['articles'][:10]:
            news_list.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'source': article['source']['name']
            })
        return news_list
    except Exception as e:
        print(f"News Error: {e}")
        return []

# === Routes ===
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    total_clients = len(set(note.client_name for note in notes))
    total_visits = len(notes)
    total_proposals = sum(1 for note in notes if note.proposal_given)
    total_sales = sum(note.sales_estimated or 0 for note in notes)
    return render_template('dashboard.html',
                           total_clients=total_clients,
                           total_visits=total_visits,
                           total_proposals=total_proposals,
                           total_sales=total_sales,
                           notes=notes[-5:])

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        content_text = request.form.get('content')
        sentiment_result = analyze_sentiment(content_text)

        new_note = Note(
            title=request.form.get('title'),
            content=content_text,
            client_name=request.form.get('client_name'),
            sales_estimated=float(request.form.get('sales_estimated') or 0),
            proposal_given='proposal_given' in request.form,
            sector=request.form.get('sector'),
            region=request.form.get('region'),
            sentiment=sentiment_result,
            user_id=current_user.id
        )
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('notes'))

    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/analytics')
@login_required
def api_get_analytics():
    user_id = current_user.id
    notes = Note.query.filter_by(user_id=user_id).all()

    sector_counts = {}
    region_counts = {}
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}

    for note in notes:
        sector_counts[note.sector] = sector_counts.get(note.sector, 0) + 1
        region_counts[note.region] = region_counts.get(note.region, 0) + 1
        if note.sentiment:
            sentiments[note.sentiment] = sentiments.get(note.sentiment, 0) + 1

    analytics = {
        'total_clients': len(set(note.client_name for note in notes)),
        'total_visits': len(notes),
        'total_proposals': sum(1 for note in notes if note.proposal_given),
        'total_sales': sum(note.sales_estimated or 0 for note in notes),
        'sector_counts': [{'sector': k, 'count': v} for k, v in sector_counts.items()],
        'region_counts': [{'region': k, 'count': v} for k, v in region_counts.items()],
        'sentiments': sentiments
    }
    return jsonify(analytics)

@app.route('/market-insights')
@login_required
def market_insights():
    return render_template('market_insights.html')

@app.route('/api/company-insights/<company_name>')
@login_required
def api_company_insights(company_name):
    data = get_company_insights(company_name)
    if "error" in data:
        return jsonify({'error': data["error"]}), 500
    return jsonify(data)

@app.route('/news')
@login_required
def news():
    market_news = fetch_market_news()
    return render_template('news.html', news_list=market_news)

# === New AI Summarizer Route ===
@app.route('/summarize', methods=['GET', 'POST'])
@login_required
def summarize_notes():
    summary = ''
    user_input = ''

    if request.method == 'POST':
        user_input = request.form['notes']

        prompt = f"Summarize the following sales meeting notes into a short summary with action points:\n\n{user_input}\n\nSummary:"

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                temperature=0.5,
            )
            summary = response.choices[0].text.strip()
        except Exception as e:
            summary = f"Error: {str(e)}"

    return render_template('summarize.html', summary=summary, user_input=user_input)

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            admin = User(
                email='admin@example.com',
                password=generate_password_hash('admin123', method='sha256')
            )
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
