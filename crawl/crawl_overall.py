import csv
from bs4 import BeautifulSoup
import os
import pandas as pd
import requests
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def extract_job_details(html_content, nhom_nghe):
    soup = html_content
    
    # Job Title
    job_title = soup.find('h3', class_='title').find('a').find('span')['data-original-title'] if soup.find('h3', class_='title') else float('nan')
    
    # Company Name
    company_name = soup.find('a', class_='company').find('span', class_='company-name').text.strip() if soup.find('a', class_='company') else float('nan')
    
    # Salary
    salary = soup.find('label', class_='title-salary').text.strip() if soup.find('label', class_='title-salary') else float('nan')
    
    # Location
    location = soup.find('label', class_='address').find('span', class_='city-text').text.strip() if soup.find('label', class_='address') else float('nan')
    
    # Experience
    experience = soup.find('label', class_='exp').find('span').text.strip() if soup.find('label', class_='exp') else float('nan')
    
    # Job Tags
    main_tags = [tag.text.strip() for tag in soup.find('div', class_='tag').find_all('span', class_='item-tag')] if soup.find('div', class_='tag') else []
    
    # Additional Tags
    additional_tags_elem = soup.find('span', class_='remaining-items')
    additional_tags = additional_tags_elem['data-original-title'].split(', ') if additional_tags_elem else []
    
    # Job Link
    job_link = soup.find('h3', class_='title').find('a')['href'] if soup.find('h3', class_='title') else float('nan')
    
    # Posted Date
    posted_date = soup.find('label', class_='address mobile-hidden label-update').text.strip() if soup.find('label', class_='address mobile-hidden label-update') else float('nan')
    
    job_id = soup.get('data-job-id')
    
    
    # Job Position (from data attribute)
    job_position = soup.get('data-job-position')
    
    return {
        'Job Title': job_title,
        'Company Name': company_name,
        'Salary': salary,
        'Location': location,
        'Experience': experience,
        'Main Tags': '; '.join(main_tags),
        'Additional Tags': '; '.join(additional_tags),
        'Job Link': job_link,
        'Posted Date': posted_date,
        'Job ID': job_id,
        'Job Position': job_position,
        'Job Category': nhom_nghe
    }

def save_to_csv(file_name, data):
    try:
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False, encoding='utf-8')
        print(f"Data successfully saved to {file_name}.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def configure_driver():
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

job_details = []
def scrape(driver, url, nhom_nghe, data_folder_path = 'data'):
    try:
        driver.get(url)
    
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job-list-search-result"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_list = soup.find('div', class_="job-list-search-result").find_all('div', class_='job-item-search-result')
            # time.sleep(1)  # Tránh bị chặn
        print(f'{len(job_list)=}')
        for job in job_list:
            try:
                job_detail = extract_job_details(job, nhom_nghe)
                # print(job)
                # return
            except Exception as e:
                print(f'ham extract_job_details loi {e}')
            job_details.append(job_detail)
        save_to_csv(f'./{data_folder_path}/data_{nhom_nghe}.csv', job_details)
    except Exception as e:
        print(f"Error scraping page: {url}. Error: {e}")

def main():
    nhomnghe = {
    'công nghệ thông tin': {'url': 'https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257?type_keyword=0', 'flag': 104},
    'kinh doanh, bán hàng': {'url': 'https://www.topcv.vn/tim-viec-lam-kinh-doanh-ban-hang-cr1?type_keyword=0', 'flag': 260},
    'marketing, pr, quảng cáo': {'url': 'https://www.topcv.vn/tim-viec-lam-marketing-pr-quang-cao-cr92?type_keyword=0', 'flag': 124},
    'dịch vụ khách hàng, vận hành': {'url': 'https://www.topcv.vn/tim-viec-lam-dich-vu-khach-hang-van-hanh-cr158?type_keyword=0', 'flag': 42},
    'nhân sự, hành chí, pháp chế': {'url': 'https://www.topcv.vn/tim-viec-lam-nhan-su-hanh-chinh-phap-che-cr177?type_keyword=0', 'flag': 71},
    'tài chính, ngân hàng, bảo hiểm': {'url': 'https://www.topcv.vn/tim-viec-lam-tai-chinh-ngan-hang-bao-hiem-cr206?type_keyword=0', 'flag': 29},
    'bất động sản, xây dựng': {'url': 'https://www.topcv.vn/tim-viec-lam-bat-dong-san-xay-dung-cr333?type_keyword=0', 'flag': 55},
    'kế toán, kiểm toán, thuế': {'url': 'https://www.topcv.vn/tim-viec-lam-ke-toan-kiem-toan-thue-cr392?type_keyword=0', 'flag': 69},
    'sản xuất': {'url': 'https://www.topcv.vn/tim-viec-lam-san-xuat-cr417?type_keyword=0', 'flag': 85},
    'giáo dục, đào tạo': {'url': 'https://www.topcv.vn/tim-viec-lam-giao-duc-dao-tao-cr477?type_keyword=0', 'flag': 64},
    'bán lẻ, dịch vụ, đời sống': {'url': 'https://www.topcv.vn/tim-viec-lam-ban-le-dich-vu-doi-song-cr544?type_keyword=0', 'flag': 83},
    'phim và truyền hình, báo chí, xuất bản': {'url': 'https://www.topcv.vn/tim-viec-lam-phim-va-truyen-hinh-bao-chi-xuat-ban-cr612?type_keyword=0', 'flag': 14},
    'điện, điện tử, viễn thông': {'url': 'https://www.topcv.vn/tim-viec-lam-dien-dien-tu-vien-thong-cr644?type_keyword=0', 'flag': 36},
    'logistic, thu mua, kho, vận tải': {'url': 'https://www.topcv.vn/tim-viec-lam-logistics-thu-mua-kho-van-tai-cr711?type_keyword=0', 'flag': 41},
    'tư vấn chuyên môn, luật, biên phiên dịch': {'url': 'https://www.topcv.vn/tim-viec-lam-tu-van-chuyen-mon-luat-bien-phien-dich-cr750?type_keyword=0', 'flag': 17},
    'dược, y tế , sức khỏe, công nghệ sinh học': {'url': 'https://www.topcv.vn/tim-viec-lam-duoc-y-te-suc-khoe-cong-nghe-sinh-hoc-cr781?type_keyword=0', 'flag': 28},
    'thiết kế': {'url': 'https://www.topcv.vn/tim-viec-lam-thiet-ke-cr826?type_keyword=0', 'flag': 54},
    'nhà hàng, khách sạn, du lịch': {'url': 'https://www.topcv.vn/tim-viec-lam-nha-hang-khach-san-du-lich-cr857?type_keyword=0', 'flag': 34},
    'năng lượng, môi trường, nông nghiệp': {'url': 'https://www.topcv.vn/tim-viec-lam-nang-luong-moi-truong-nong-nghiep-cr883?type_keyword=0', 'flag': 7},
    'nhóm nghề khác': {'url': 'https://www.topcv.vn/tim-viec-lam-nhom-nghe-khac-cr899?type_keyword=0', 'flag': 5},
    'tài xế': {'url': 'https://www.topcv.vn/tim-viec-lam-tai-xe-cr1010?type_keyword=0', 'flag': 5},
    }

    if len(sys.argv) != 5:
        print("Usage: python run.py <job_category> <start_page> <end_page> <data_folder_path>")
        sys.exit(1)

    job_category = sys.argv[1]
    try:
        start_page = int(sys.argv[2])
        end_page = int(sys.argv[3])
    except ValueError:
        print("Error: start_page and end_page must be integers.")
        sys.exit(1)

    data_folder_path = sys.argv[4]

    if job_category not in nhomnghe:
        print(f"Error: job_category '{job_category}' not found in the predefined list.")
        sys.exit(1)

    data = nhomnghe[job_category]
    url = data['url']

    options = configure_driver()

    try:
        for page in range(start_page, end_page + 1):
            driver = webdriver.Chrome(options=options)
            current_url = f"{url}&page={page}"
            print(f"Scraping page {page}: {current_url}")
            scrape(driver, current_url, job_category, data_folder_path)
            driver.quit()

    finally:
        print("Scraping completed.")

if __name__ == "__main__":
    main()

#python overall.py "kinh doanh, bán hàng" 1 5 "data"
