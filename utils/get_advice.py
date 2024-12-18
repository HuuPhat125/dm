import os
import time
import google.generativeai as genai

def verify_response(response):
    if response == "" or response is None:
        return 'An error occurred, please try again later'
    if "429 Quota exceeded for quota metric" in response:
        return 'An error occurred, please try again later'
    if isinstance(response, str):
        response = response.strip()
    return response
class Gemini_Model:
    def __init__(self, key, model_name="gemini-1.5-flash", patience=1, sleep_time=5):
        self.patience = patience
        self.sleep_time = sleep_time
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(model_name=model_name)

    def get_response(self, query):
        patience = self.patience
        while patience > 0:
            patience -= 1
            try:
                response = self.model.generate_content(query)
                response_text = response.text.strip()
                return verify_response(response_text)
                     
            except Exception as e:
                if self.sleep_time > 0:
                    time.sleep(self.sleep_time)
        return 'An error occurred, please try again later'

api_key = os.getenv("API_KEY")
model = Gemini_Model(api_key)

def get_job_advice(job_requirements, experiences_query):
    if experiences_query == '':
        return 'Please enter the your experiences to get the usefull advice'
    # job_requirements = job_details['Requirements']
    prompt = f'''
            Base on job requirements and user experiences, give an usefull advice, what user need to improve to meet job requirements.
            job requirements: {job_requirements}.
            user experiences: {experiences_query}.
            Advice:
        '''
    advice = model.get_response(prompt)
    return advice