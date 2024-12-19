import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

def plot_salary_distribution(df, category="công nghệ thông tin"):
    """
    Plot the salary distribution for a specific job category.
    Returns the Matplotlib figure object for rendering in web applications.
    """
    df_new = df[
        (df['Job Category'] == category) &
        (df['min_salary'] <= 100) & 
        (df['max_salary'] <= 100)
    ]
    salaries = []
    for _, row in df_new.iterrows():
        min_salary = row['min_salary']
        max_salary = row['max_salary']
        if min_salary >= 0 and max_salary >= 0:
            salaries.extend(np.arange(min_salary, max_salary + 1))
        elif min_salary >= 0:
            salaries.append(min_salary)
        elif max_salary >= 0:
            salaries.append(max_salary)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))  # Tạo Figure và Axes
    sns.histplot(salaries, bins=np.arange(0, 101, 1), kde=True, color="blue", ax=ax)
    ax.set_xlim(0, 100)
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_title(f'Salary Distribution for {category}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Salary (in millions)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    return fig  # Trả về Figure
    
def plot_avg_salary(df, top_k=5, category='Job Category', by_max_salary=False):
    """
    Returns a Matplotlib figure object for rendering in web applications.
    """
    # Lọc bỏ các giá trị ngoài phạm vi
    df_filtered = df[
        (df['min_salary'] <= 100) &
        (df['max_salary'] <= 100)
    ]
    
    # Xử lý giá trị -1 riêng cho từng cột
    df_filtered['min_salary'] = df_filtered['min_salary'].replace(-1, pd.NA)
    df_filtered['max_salary'] = df_filtered['max_salary'].replace(-1, pd.NA)
    
    # Tính tiền lương trung bình cho từng ngành nghề
    avg_salary = df_filtered.groupby(category).agg(
        avg_min_salary=('min_salary', 'mean'),
        avg_max_salary=('max_salary', 'mean')
    ).reset_index()

    # Chuyển đổi kiểu dữ liệu của avg_max_salary và avg_min_salary sang kiểu float
    avg_salary['avg_min_salary'] = pd.to_numeric(avg_salary['avg_min_salary'], errors='coerce')
    avg_salary['avg_max_salary'] = pd.to_numeric(avg_salary['avg_max_salary'], errors='coerce')
    
    # Lọc ra top-k ngành nghề phổ biến nhất hoặc top-k theo max_salary
    if by_max_salary:
        avg_salary_filtered = avg_salary.nlargest(top_k, 'avg_max_salary')
    else:
        job_count = df_filtered[category].value_counts().head(top_k).index
        avg_salary_filtered = avg_salary[avg_salary[category].isin(job_count)]
    
    # Kiểm tra dữ liệu
    if avg_salary_filtered.empty:
        print("No data available for plotting after filtering.")
        return None

    # Vẽ biểu đồ cột đôi
    x = avg_salary_filtered[category]
    min_salary = avg_salary_filtered['avg_min_salary']
    max_salary = avg_salary_filtered['avg_max_salary']
    
    x_indices = range(len(x))
    
    # Tạo Figure và Axes
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x_indices, min_salary, width=0.4, label='Min Salary', color='skyblue', align='center')
    ax.bar([i + 0.4 for i in x_indices], max_salary, width=0.4, label='Max Salary', color='lightgreen', align='center')

    ax.set_xticks([i + 0.2 for i in x_indices])
    ax.set_xticklabels(x, rotation=45)
    ax.set_xlabel('Job Category')
    ax.set_ylabel('Salary (Millions VND)')
    ax.set_title(f'Average Salary by {category} (Top {top_k} Popular){" with Max Salary" if by_max_salary else ""}')
    ax.legend()
    plt.tight_layout()

    return fig  # Trả về Figure


def plot_avg_salary_by_tag(df, top_k=10, category=None):
    """
    Vẽ biểu đồ tiền lương trung bình (min_salary và max_salary) theo từng tag.
    
    Args:
        df (pd.DataFrame): DataFrame chứa các cột 'new_tags', 'min_salary', 'max_salary', và 'Job Category'.
        top_k (int): Số lượng tag phổ biến nhất để hiển thị.
        category (str, optional): Tên của một ngành cụ thể để lọc. Nếu không có, tính trên tất cả các ngành.
    """
    df = df.copy()

    # Lọc theo category nếu được chỉ định
    if category:
        df = df[df['Job Category'] == category]

    # Chuyển cột 'min_salary' và 'max_salary' sang kiểu số
    df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce')
    df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce')

    # Tách cột new_tags theo dấu ";"
    df['new_tags'] = df['new_tags'].str.split(';')
    df_exploded = df.explode('new_tags')
    df_exploded['new_tags'] = df_exploded['new_tags'].str.strip()  # Loại bỏ khoảng trắng thừa

    # Tính tiền lương trung bình cho từng tag
    avg_salary = df_exploded.groupby('new_tags').agg(
        avg_min_salary=('min_salary', 'mean'),
        avg_max_salary=('max_salary', 'mean')
    ).reset_index()

    # Chuyển đổi kiểu dữ liệu sang số (phòng ngừa lỗi kiểu dữ liệu)
    avg_salary['avg_min_salary'] = pd.to_numeric(avg_salary['avg_min_salary'], errors='coerce')
    avg_salary['avg_max_salary'] = pd.to_numeric(avg_salary['avg_max_salary'], errors='coerce')

    # Lấy top-k tag có giá trị tiền lương trung bình cao nhất (theo avg_max_salary)
    avg_salary = avg_salary.nlargest(top_k, 'avg_max_salary')

    # Kiểm tra dữ liệu
    if avg_salary.empty:
        print("No data available for plotting.")
        return None

    # Tạo Figure và Axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Vẽ biểu đồ cột đôi cho avg_min_salary và avg_max_salary
    x = avg_salary['new_tags']
    min_salary = avg_salary['avg_min_salary']
    max_salary = avg_salary['avg_max_salary']

    x_indices = range(len(x))
    ax.bar(x_indices, min_salary, width=0.4, label='Avg Min Salary', color='skyblue', align='center')
    ax.bar([i + 0.4 for i in x_indices], max_salary, width=0.4, label='Avg Max Salary', color='lightgreen', align='center')

    # Thiết lập nhãn trục và tiêu đề
    ax.set_xticks([i + 0.2 for i in x_indices])
    ax.set_xticklabels(x, rotation=45, ha='right')
    ax.set_xlabel('Tags')
    ax.set_ylabel('Salary (Millions VND)')
    title = f'Average Salary by Tags (Top {top_k})'
    if category:
        title += f' for {category}'
    ax.set_title(title)
    ax.legend()

    plt.tight_layout()
    return fig


import matplotlib.pyplot as plt
import seaborn as sns

def avg_salary_by_experience(df, job_category=None):
    df['min_salary'] = df['min_salary'].replace(-1.0, float('nan'))
    df['max_salary'] = df['max_salary'].replace(-1.0, float('nan'))
    df['avg_salary'] = df[['min_salary', 'max_salary']].mean(axis=1)

    if job_category is not None:
        df = df[df['Job Category'] == job_category]

    role_counts = df['Job Category'].value_counts().head(5).index

    top_roles = df[df['Job Category'].isin(role_counts)]

    avg_salary_by_role_exp = (
        top_roles
        .groupby(['Experience', 'Job Category'])['avg_salary']
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='Experience', y='avg_salary', hue='Job Category', data=avg_salary_by_role_exp, marker='o', ax=ax)
    ax.set_title('year of experience by year of experience')
    ax.set_xlabel('year of experience')
    ax.set_ylabel('year of experience (milVNĐ)')
    ax.set_xticks(range(int(avg_salary_by_role_exp['Experience'].min()), int(avg_salary_by_role_exp['Experience'].max()) + 1))
    ax.legend(title='Job Category')
    ax.grid(True)

    return fig
