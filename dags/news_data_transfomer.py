import json
import csv
from datetime import datetime

def categorize_title(title):
    categories = {
        "Entertainment": ["entertainment", "movie", "film", "music"],
        "Lifestyle": ["lifestyle", "health", "wellness", "food"],
        "Local news": ["local", "community","shooting"],
        "Business journalism": ["business", "finance","market","economy","struggle"],
        "Health": ["health", "medical", "wellness"],
        "Politics": ["politics", "government", "election","Trump","Washington","Democrats","campaign"],
        "Science": ["science", "technology", "research","tech"],
        "Sports": ["sports", "game", "match"],
        "Press releases": ["press", "release","Journal"]
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title.lower():
                return category
    return "Uncategorized"

def transform_news_data(news_data):
    transformed_data = []
    
    for article in news_data['articles']:
        title = article['title']
        category = categorize_title(title)
        author = article['author']
        source = article['source']['name']
        published_at = article['publishedAt']
        url = article['url']
        
        transformed_data.append({
            'category': category,
            'title': title,
            'author': author,
            'source': source,
            'publishedAt': published_at,
            'url': url
        })
    
    return transformed_data

def save_to_csv(transformed_data, file_name_prefix):
    date_time_now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_name = f"{file_name_prefix}_{date_time_now}.csv"
    file_path = f"/opt/airflow/dags/temp/{file_name}" 
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'category', 'author', 'source', 'publishedAt', 'url'])
        writer.writeheader()
        for data in transformed_data:
            writer.writerow(data)
    
    return file_path