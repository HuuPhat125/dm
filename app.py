import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

from utils.tab4 import plot_salary_distribution, plot_avg_salary, plot_avg_salary_by_tag
# Thiết lập theme và layout
st.set_page_config(
    page_title="Job Market Insights", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tùy chỉnh CSS
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    font-weight: bold;
    color: #2C3E50;
}
.highlight {
    background-color: #F1F8FF;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: #E8F4F8;
    color: #2C3E50;
    border-radius: 10px;
    font-weight: bold;
}
.stTabs [data-baseweb="tab"][data-selected="true"] {
    background-color: #3498DB;
    color: white;
}
                        
</style>
""", unsafe_allow_html=True)

def load_data():
    """Tải dữ liệu và xử lý"""
    df = pd.read_csv('preprocessed_P_unique_job.csv')
    return df

def create_job_distribution_plot(df, group_by, top_k=5):
    """Tạo biểu đồ phân phối công việc với Plotly"""
    if group_by == "new_tags":
        job_category = st.selectbox(
            "Select Job Category for Tags Analysis", 
            ['All'] + list(df['Job Category'].unique())
        )
        if job_category == 'All': 
            df_filtered = df
        else: 
            df_filtered = df[df['Job Category'] == job_category]
        
        df_filtered['new_tags'] = df_filtered['new_tags'].str.split(';')
        df_exploded = df_filtered.explode('new_tags')
        counts = df_exploded['new_tags'].value_counts()
    else:
        counts = df[group_by].value_counts()

    # Chọn top k và nhóm "Khác"
    counts_top = counts.head(top_k)
    other_count = counts[top_k:].sum()
    counts_top["Others"] = other_count

    # Tạo biểu đồ Plotly
    fig = px.pie(
        values=counts_top.values, 
        names=counts_top.index, 
        title=f"Distribution of Jobs by {group_by}",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    return fig

def create_top_companies_plot(df, top_k=5):
    """Tạo biểu đồ các công ty hàng đầu"""
    top_companies = df['Company Name'].value_counts().head(top_k)
    
    fig = px.bar(
        x=top_companies.index, 
        y=top_companies.values,
        title=f"Top {top_k} Companies by Job Postings",
        labels={'x': 'Company Name', 'y': 'Number of Jobs'},
        color=top_companies.values,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        xaxis_title="Company Name", 
        yaxis_title="Number of Jobs"
    )
    return fig

def interactive_job_filter(df):
    
    # Tạo các cột để lọc
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        location = st.selectbox("Location", 
            ['All'] + list(df['Location'].unique()))
    
    with col2:
        experience = st.selectbox("Experience Level", 
            ['All'] + list(df['Experience'].unique()))
    
    with col3:
        category = st.selectbox("Job Category", 
            ['All'] + list(df['Job Category'].unique()))
    
    with col4:
        df['new_tags'] = df['new_tags'].fillna('').astype(str)
        tag = st.selectbox("Tags", 
            ['All'] + list(set(tag for tags in df['new_tags'].str.split(';') for tag in tags)))
    
    # Lọc dữ liệu
    filtered_df = df.copy()
    if location != 'All':
        filtered_df = filtered_df[filtered_df['Location'] == location]
    if experience != 'All':
        filtered_df = filtered_df[filtered_df['Experience'] == experience]
    if category != 'All':
        filtered_df = filtered_df[filtered_df['Job Category'] == category]
    if tag != 'All':
        filtered_df = filtered_df[filtered_df['new_tags'].str.contains(tag, na=False)]
    
    # Hiển thị kết quả
    st.write(f"📊 Found {len(filtered_df)} jobs")
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.warning("No jobs found matching the selected filters.")

def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🌐 Job Market Explorer</h1>", unsafe_allow_html=True)
    
    # Load dữ liệu
    df = load_data()
    
    # Tạo tab
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Job Distribution", "🏢 Company Insights", "🔍 Job Search", "💸 Explore Salary"])
    
    with tab1:
        st.subheader("📊 Job Distribution Analysis")

        col1, col2 = st.columns(2)
        with col1:
            group_by = st.selectbox("Group Jobs By", 
                ["Job Category", "Location", "Experience", "new_tags"])
        with col2:
            top_k = st.slider("Top Categories", 3, 50, 10)
        
        fig = create_job_distribution_plot(df, group_by, top_k)
        fig.update_layout(width=1200, height=800) 
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.subheader("🏢 Top Companies Insights")

        top_k = st.slider("Number of Top Companies", 3, 10, 5)
        fig_companies = create_top_companies_plot(df, top_k)
        st.plotly_chart(fig_companies, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        # st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.subheader("🔍 Interactive Job Filter")
        interactive_job_filter(df)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.subheader("💸 Explore Salary")

        sub_tab1 = st.selectbox("What do you want to explore", ["Salary distribution", "Average salary", "Average on tags"])
    
        if sub_tab1 == "Salary distribution":
            category = st.selectbox("Select a job category to view the salary distribution", list(df['Job Category'].unique()))
            fig = plot_salary_distribution(df, category=category)
            st.pyplot(fig)
        elif sub_tab1 == "Average salary":
            col1, col2, col3 = st.columns(3)
            with col1:
                feature = st.selectbox("Select a feature to view the average salary.", ["Job Category", "Location", "Experience"])
            with col2:
                sort_by = st.selectbox("Sort by.", ["Salary", "Feature"])
                sort_by = True if sort_by == 'Salary' else False
            with col3:
                topk = st.slider("Top k popular", 3, 10, 5)
            fig = plot_avg_salary(df, top_k=topk, category=feature, by_max_salary=sort_by)
            st.pyplot(fig)
        elif sub_tab1 ==  "Average on tags":
            col1, col2 = st.columns(2)
            with col1:
                job_cat = st.selectbox("Select a job category to view the salary distribution", ['All'] + list(df['Job Category'].unique()))
                job_cat = None if job_cat == 'All' else job_cat
            with col2:
                topk = st.slider("Select top k to show", 3, 10, 5)
            fig = plot_avg_salary_by_tag(df,top_k=topk, category=job_cat)
            st.pyplot(fig)
if __name__ == '__main__':
    main()