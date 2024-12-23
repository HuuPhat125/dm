## Overview
This project focuses on leveraging data from TopCV to build predictive and recommendation systems. By crawling job postings and resumes from the platform, we aim to develop:

1. **Salary Prediction Model**: A machine learning model to estimate salary ranges based on job descriptions and candidate profiles.
2. **Job Recommendation System**: A system that matches job seekers with the most relevant job postings based on their skills, experiences, and preferences.

## Objectives
- **Data Collection**: Crawl job postings and resumes from TopCV.
- **Data Analysis**: Analyze the crawled data to extract meaningful insights.
- **Model Development**:
  - Train a salary prediction model.
  - Build a personalized job recommendation system.
- **Deployment**: Provide a user-friendly interface for interacting with the models.

## Features
1. **Data Crawling**:
   - Automated scraping of job postings.
   - Storage of structured data for analysis and modeling.

2. **Salary Prediction**:
   - Predict salary ranges based on features like job category, location, required skills, and experience.

3. **Job Recommendation**:
   - Personalized recommendations for job seekers.
   - Ranking of job postings based on relevance.

4. **Get advide**:
   - Base on your experiences and job requirements, the model will give you personal advices, the model tell you what do you need to learn to meet the job requirements.
  
5. **Data Visualization**:
   - Graphical representation of job trends, salary distributions, and demand for skills.

## Dataset
- **Source**: TopCV job postings.
- **Structure**:
  - **Job Postings**: Job title, company, location, salary range, job description, required skills.

## Workflow
1. **Crawling**:
   - Use web scraping tools to collect data.
   - Ensure compliance with TopCV’s terms of service.
2. **Data Preprocessing**:
   - Clean and normalize the data.
   - Handle missing or inconsistent values.
3. **Exploratory Data Analysis (EDA)**:
   - Analyze job trends and skills demand.
   - Visualize salary distributions and other key metrics.
4. **Model Training**:
   - Train the salary prediction model using regression techniques.
   - Build the recommendation system using collaborative filtering or content-based approaches.
5. **Evaluation**:
   - Evaluate models using metrics like RMSE for salary prediction and precision/recall for recommendations.
6. **Deployment**:
   - Develop an interactive web interface or API for accessing the models.

## Technology Stack
- **Programming Languages**: Python
- **Libraries/Frameworks**:
  - **Data Crawling**: BeautifulSoup, Scrapy
  - **Data Analysis**: Pandas, NumPy, Matplotlib, Seaborn
  - **Machine Learning**: scikit-learn, TensorFlow/PyTorch
  - **Web Development**: Streamlit
## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HuuPhat125/jobs-analysis-and-recommendation.git
   cd jobs-analysis-and-recommendation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables for crawling (e.g., API keys, user agents).

## Usage
1. **Crawling Data**:
   ```bash
   crawl/crawl_overall.py
   crawl/crawl_detail.py
   ```
2. **Training Models**:

3. **Running the Application**:
   ```bash
   streamlit run app.py
   ```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- **TopCV** for the data source.
- Open-source libraries and frameworks.

## Contact
For questions or suggestions, please contact [phatd142@gmail.com].


## Group 8
| Họ và tên       | MSSV       | Công việc       |Khối lượng công việc(%)| Mức độ hoàn thành
|----------------|----------------|----------------|----------------|----------------|
| Đặng Hữu Phát  | 22521065  | - Crawl dataset <br>- EDA <br>- Soạn slide <br>- Code demo thực nghiệm| 33%|100%
| Phan Nguyễn Hữu Phong  |  22521090  | - Huấn luyện mô hình  <br>- Soạn slide <br>- Viết báo cáo <br>- Code demo thực nghiệm|33%|100%
| Phạm Quang Nhựt  | 22521061  | - Thuyết trình<br>- Tiền xử lý dữ liệu <br>- Soạn slide <br>- Viết báo cáo <br>|33%|100%
