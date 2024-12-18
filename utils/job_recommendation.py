import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator


def find_top_k_jobs(df, description_query, requirements_query, benefits_query, k=5):
    """
    Find the top-k jobs based on the similarity of description, requirements, and benefits.
    Handles None for any of the queries by skipping their respective similarity calculations.
    Automatically detects the language of the queries and translates them to English if needed.

    Args:
        description_query (str or None): Query for job description.
        requirements_query (str or None): Query for job requirements.
        benefits_query (str or None): Query for job benefits.
        k (int): Number of top results to return.

    Returns:
        pd.DataFrame: Top-k job postings sorted by average similarity score.
    """

    tfidf = TfidfVectorizer(stop_words='english')

    def translate_to_english(query):
        if query is not None:
            return GoogleTranslator(source='auto', target='en').translate(query)
        return query

    description_query = translate_to_english(description_query)
    requirements_query = translate_to_english(requirements_query)
    benefits_query = translate_to_english(benefits_query)

    scores_list = []

    # Process Description
    if description_query is not None:
        print(f'{description_query=}')
        tfidf_description = tfidf.fit_transform(df['E_Description'].fillna(''))
        description_vector = tfidf.transform([description_query])
        description_scores = cosine_similarity(description_vector, tfidf_description).flatten()
        scores_list.append(description_scores)

    # Process Requirements
    if requirements_query is not None:
        print(f'{requirements_query=}')
        tfidf_requirements = tfidf.fit_transform(df['E_Requirements'].fillna(''))
        requirements_vector = tfidf.transform([requirements_query])
        requirements_scores = cosine_similarity(requirements_vector, tfidf_requirements).flatten()
        scores_list.append(requirements_scores)

    # Process Benefits
    if benefits_query is not None:
        print(f'{benefits_query=}')
        tfidf_benefits = tfidf.fit_transform(df['E_Benefits'].fillna(''))
        benefits_vector = tfidf.transform([benefits_query])
        benefits_scores = cosine_similarity(benefits_vector, tfidf_benefits).flatten()
        scores_list.append(benefits_scores)

    # Calculate average similarity if there are scores to combine
    if scores_list:
        average_scores = np.mean(scores_list, axis=0)
        top_k_indices = average_scores.argsort()[-k:][::-1]
        return df.iloc[top_k_indices]
    else:
        # If no valid queries are provided, return an empty DataFrame
        return df.iloc[[]]


# description_query = 'triển khai các mô hình NLP, RAG, nghiên cứu phát triển sản phẩm mới để tích hợp vào hệ thống phần mềm' # muốn làm công việc gì,  
# #'Deploy AI model, research and develop new products to integrate into the software system'
# requirements_query = None # có kinh nghiệm gì, đã làm gì,..
# # 'Proficient in English communication skills'
# benefits_query = None # muốn có lợi ích gì, muốn nhận được gì từ công ty,...
# #'Annual insurance, salary increase every two years'

# result = find_top_k_jobs(description_query, requirements_query, benefits_query, k=5)
# result #3468 2524