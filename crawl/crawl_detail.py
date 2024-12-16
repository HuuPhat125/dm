from bs4 import BeautifulSoup
import sys
import json
from tqdm import tqdm
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def extract_job_details(soup):
    
    # Extract job title
    job_title = soup.find('h1', class_='job-detail__info--title').get_text(strip=True) if soup.find('h1', class_='job-detail__info--title') else 'N/A'
    
    # Extract salary
    salary = soup.find('div', class_='job-detail__info--section-content-value')
    salary = salary.get_text(strip=True) if salary else 'N/A'
    
    # Extract location
    location = soup.find_all('div', class_='job-detail__info--section-content-value')[1]
    location = location.get_text(strip=True) if location else 'N/A'
    
    # Extract experience
    experience = soup.find('div', id='job-detail-info-experience')
    experience = experience.find('div', class_='job-detail__info--section-content-value').get_text(strip=True) if experience else 'N/A'
    
    # Extract application deadline
    deadline = soup.find('div', class_='job-detail__info--deadline')
    deadline = deadline.get_text(strip=True).replace('Hạn nộp hồ sơ: ', '') if deadline else 'N/A'
    
    # Return a dictionary of extracted information
    return {
        'Job Title': job_title,
        'Salary': salary,
        'Location': location,
        'Experience Required': experience
    }

def extract_job_description(soup):
    
    # Job Tags
    job_tags = [tag.get_text(strip=True) for tag in soup.find_all('a', class_='item search-from-tag')]
    
    # Job Description Sections
    job_sections = {}
    for section in soup.find_all('div', class_='job-description__item'):
        title = section.find('h3').get_text(strip=True)
        content = [p.get_text(strip=True) for p in section.find_all('p')]
        if len(content) != 0:
            job_sections[title] = content
        else:
            content = [li.get_text(strip=True) for li in section.find_all('li')]
            job_sections[title] = content
    # Work Locations
    locations = [loc.get_text(strip=True) for loc in soup.find_all('div', style='margin-bottom: 10px')]
    
    # Deadline
    deadline = soup.find('div', class_='job-detail__information-detail--actions-label')
    deadline = deadline.get_text(strip=True).replace('Hạn nộp hồ sơ: ', '') if deadline else 'N/A'
    
    return {
        'Job Tags': job_tags,
        'Job Description Sections': job_sections,
        'Work Locations': locations,
        'Application Deadline': deadline
    }


def get_overall(soup):

    # Company Information
    company_logo = soup.find('img', class_='img-responsive')['src'] if soup.find('img', class_='img-responsive') else None
    company_name = soup.find('h2', class_="company-name-label").text.strip() if soup.find('h2', class_="company-name-label") else None

    # Company Details
    company_details = {}
    company_info_items = soup.find_all('div', class_='job-detail__company--information-item')
    for item in company_info_items:
        title = item.find('div', class_='company-title').text.strip() if item.find('div', class_='company-title') else None
        value = item.find('div', class_='company-value').text.strip() if item.find('div', class_='company-value') else None
        if title and value:
            company_details[title] = value

    # General Job Information
    general_info = {}
    general_groups = soup.find_all('div', class_='box-general-group')
    for group in general_groups:
        title = group.find('div', class_='box-general-group-info-title').text.strip() if group.find('div', class_='box-general-group-info-title') else None
        value = group.find('div', class_='box-general-group-info-value').text.strip() if group.find('div', class_='box-general-group-info-value') else None
        if title and value:
            general_info[title] = value

    # Related Categories
    related_categories = {}
    category_boxes = soup.find_all('div', class_='box-category')
    for box in category_boxes:
        category_name = box.find('div', class_='box-title').text.strip() if box.find('div', class_='box-title') else None
        category_tags = [tag.text.strip() for tag in box.find_all('a', class_='box-category-tag')]
        if category_name and category_tags:
            related_categories[category_name] = category_tags

    # Compile all extracted information
    job_details = {
        'Company_Name': company_name,
        'Company_Logo': company_logo,
        'Company_Details': company_details,
        'Job Information': general_info,
        'Related Categories': related_categories
    }
    return job_details

def get_all(soup):
    detail = extract_job_details(soup)
    des = extract_job_description(soup)
    over = get_overall(soup)
    return {**detail, **des, **over}
    

def configure_webdriver():
    """Cấu hình Selenium WebDriver."""
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    options.add_argument(f"user-agent={user_agent}")

    return options

def scrape_jobs(csv_path, job_category, output_dir):
    """Hàm chính để scrape dữ liệu công việc từ file CSV."""
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(csv_path)

    # Lọc các liên kết công việc theo danh mục
    job_links = df[df['Job Category'] == job_category]['Job Link'].to_list()
    print(f"====================== Start scraping '{job_category}' ======================")
    print(f"{len(job_links)} jobs found.")

    results = []
    error_links = []
    options = configure_webdriver()

    for job_link in tqdm(job_links, desc=f'Crawling {job_category}'):
        driver = webdriver.Chrome(options=options)
        driver.get(job_link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            res = get_all(soup)
            res['job_link'] = job_link
        except Exception as e:
            res = {'job_link': job_link, 'error': str(e)}
            error_links.append(job_link)
            print(f"Error scraping {job_link}: {e}")
        finally:
            results.append(res)
            driver.quit()

    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)

    # Lưu kết quả vào file JSON
    output_file = os.path.join(output_dir, f"{job_category}_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    # Lưu các liên kết lỗi (nếu có)
    if error_links:
        error_file = os.path.join(output_dir, f"{job_category}_errors.txt")
        with open(error_file, 'w', encoding='utf-8') as f:
            f.writelines(f"{link}\n" for link in error_links)

    print(f"Done! Results saved to {output_file}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <csv_path> <job_category> <output_dir>")
        sys.exit(1)

    csv_path = sys.argv[1]
    job_category = sys.argv[2]
    output_dir = sys.argv[3]

    scrape_jobs(csv_path, job_category, output_dir)

if __name__ == "__main__":
    main()


#python crawl_detail.py './data/unique_job.csv' 'công nghệ thông tin' 'detail_data'
