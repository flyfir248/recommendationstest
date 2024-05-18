from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the data
data = pd.read_csv('tbl_user_activity_data.csv')  # Replace 'your_data.csv' with the path to your CSV file


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_input = request.form['search_input']
        user_id = request.form['user_id']

        # Filter data based on user ID
        user_data = data[data['user_id'] == int(user_id)]

        # Combine product title and product breadcrumb into a single text column
        user_data['product_text'] = user_data['product_title'] + ' ' + user_data['product_breadcrumb']

        # TF-IDF Vectorization
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(user_data['product_text'].values.astype('U'))

        # Calculate similarity scores
        search_vec = tfidf_vectorizer.transform([search_input])
        similarity_scores = cosine_similarity(search_vec, tfidf_matrix)

        # Get indices of top 5 similar products
        top_indices = similarity_scores.argsort()[:, ::-1][:, :5]

        # Get recommended products
        recommendations = user_data.iloc[top_indices[0]]

        # Convert recommendations DataFrame to a list of dictionaries
        recommendations = recommendations.to_dict(orient='records')

        return render_template('index.html', search_input=search_input, user_id=user_id,
                               recommendations=recommendations)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
