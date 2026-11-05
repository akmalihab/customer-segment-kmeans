import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
MODELS_DIR = PROJECT_ROOT / 'models'
DATA_DIR = PROJECT_ROOT / 'data'

KMEANS_MODEL_PKL = MODELS_DIR / 'kmeans_model.pkl'
SCALER_PKL = MODELS_DIR / 'scaler.pkl'
LABEL_ENCODER_PKL = MODELS_DIR / 'label_encoder.pkl'
CUSTOMER_SEGMENTS_CSV = DATA_DIR / 'processed' / 'customer_segments.csv'
MALL_CUSTOMERS_CSV = DATA_DIR / 'raw' / 'Mall_Customers.csv'

st.set_page_config(page_title="Customer Segmentation", layout="wide")

# Load artifacts
@st.cache_resource
def load_model():
    with open(KMEANS_MODEL_PKL, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PKL, 'rb') as f:
        scaler = pickle.load(f)
    with open(LABEL_ENCODER_PKL, 'rb') as f:
        le = pickle.load(f)
    return model, scaler, le

@st.cache_data
def load_data():
    df = pd.read_csv(CUSTOMER_SEGMENTS_CSV)
    df_original = pd.read_csv(MALL_CUSTOMERS_CSV)
    return df, df_original

model, scaler, le = load_model()
df, df_original = load_data()

# Sidebar
st.sidebar.title("Customer Segmentation")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Overview", "Data Analysis", "Clustering Results", "Prediction Tool"])

# Define cluster labels
cluster_names = {
    0: "High Income, High Spenders",
    1: "High Income, Low Spenders", 
    2: "Middle Age, Average",
    3: "Young, Moderate Spenders",
    4: "Older, Conservative"
}

if page == "Overview":
    st.title("Customer Segmentation Analysis")
    st.markdown("### K-Means Clustering on Mall Customer Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", len(df))
    with col2:
        st.metric("Number of Clusters", model.n_clusters)
    with col3:
        st.metric("Features Used", 4)
    with col4:
        st.metric("Silhouette Score", "0.304")
    
    st.markdown("---")
    
    st.subheader("Dataset Overview")
    st.dataframe(df_original.head(10), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Statistical Summary")
        st.dataframe(df_original.describe(), use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Cluster Distribution")
        cluster_dist = df['Cluster'].value_counts().sort_index()
        cluster_dist.index = [cluster_names[i] for i in cluster_dist.index]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = plt.cm.viridis(np.linspace(0, 1, len(cluster_dist)))
        ax.bar(range(len(cluster_dist)), cluster_dist.values, color=colors)
        ax.set_xticks(range(len(cluster_dist)))
        ax.set_xticklabels(cluster_dist.index, rotation=45, ha='right')
        ax.set_ylabel('Count')
        ax.set_title('Customers per Segment')
        plt.tight_layout()
        st.pyplot(fig)

elif page == "Data Analysis":
    st.title("Exploratory Data Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Distributions", "Correlations", "Comparisons"])
    
    with tab1:
        st.subheader("Feature Distributions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(df_original['Age'], bins=20, color='skyblue', edgecolor='black')
            ax.set_xlabel('Age')
            ax.set_ylabel('Frequency')
            ax.set_title('Age Distribution')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(df_original['Annual Income (k$)'], bins=20, color='lightgreen', edgecolor='black')
            ax.set_xlabel('Income (k$)')
            ax.set_ylabel('Frequency')
            ax.set_title('Income Distribution')
            st.pyplot(fig)
        
        with col3:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.hist(df_original['Spending Score (1-100)'], bins=20, color='salmon', edgecolor='black')
            ax.set_xlabel('Spending Score')
            ax.set_ylabel('Frequency')
            ax.set_title('Spending Distribution')
            st.pyplot(fig)
    
    with tab2:
        st.subheader("Correlation Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            corr_matrix = df_original[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
            ax.set_title('Correlation Heatmap')
            st.pyplot(fig)
        
        with col2:
            st.write("**Correlation Insights:**")
            st.write("- Age vs Income: -0.012 (no correlation)")
            st.write("- Age vs Spending: -0.327 (negative correlation)")
            st.write("- Income vs Spending: 0.010 (no correlation)")
            st.write("")
            st.info("Younger customers tend to have higher spending scores, while income shows minimal correlation with spending behavior.")
    
    with tab3:
        st.subheader("Gender Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender_counts = df_original['Gender'].value_counts()
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = ['lightblue', 'pink']
            ax.bar(gender_counts.index, gender_counts.values, color=colors)
            ax.set_xlabel('Gender')
            ax.set_ylabel('Count')
            ax.set_title('Gender Distribution')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4))
            df_original.boxplot(column='Spending Score (1-100)', by='Gender', ax=ax)
            ax.set_xlabel('Gender')
            ax.set_ylabel('Spending Score')
            ax.set_title('Spending Score by Gender')
            plt.suptitle('')
            st.pyplot(fig)

elif page == "Clustering Results":
    st.title("Customer Segmentation Results")
    
    tab1, tab2, tab3 = st.tabs(["Cluster Visualization", "Segment Profiles", "Model Metrics"])
    
    with tab1:
        st.subheader("Customer Segments Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'],
                               c=df['Cluster'], cmap='viridis', s=80, alpha=0.6, edgecolors='black')
            
            centers_income = model.cluster_centers_[:, 1] * scaler.scale_[1] + scaler.mean_[1]
            centers_spending = model.cluster_centers_[:, 2] * scaler.scale_[2] + scaler.mean_[2]
            ax.scatter(centers_income, centers_spending,
                      c='red', s=300, alpha=0.8, marker='X', edgecolors='black', linewidths=2)
            
            ax.set_xlabel('Annual Income (k$)', fontsize=12)
            ax.set_ylabel('Spending Score (1-100)', fontsize=12)
            ax.set_title('Income vs Spending Score', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax, label='Cluster')
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(df['Age'], df['Spending Score (1-100)'],
                               c=df['Cluster'], cmap='viridis', s=80, alpha=0.6, edgecolors='black')
            
            centers_age = model.cluster_centers_[:, 0] * scaler.scale_[0] + scaler.mean_[0]
            ax.scatter(centers_age, centers_spending,
                      c='red', s=300, alpha=0.8, marker='X', edgecolors='black', linewidths=2)
            
            ax.set_xlabel('Age', fontsize=12)
            ax.set_ylabel('Spending Score (1-100)', fontsize=12)
            ax.set_title('Age vs Spending Score', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax, label='Cluster')
            st.pyplot(fig)
        
        st.markdown("---")
        
        st.subheader("3D Visualization")
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(df['Age'], df['Annual Income (k$)'], df['Spending Score (1-100)'],
                           c=df['Cluster'], cmap='viridis', s=60, alpha=0.6, edgecolors='black')
        ax.set_xlabel('Age')
        ax.set_ylabel('Annual Income (k$)')
        ax.set_zlabel('Spending Score (1-100)')
        ax.set_title('3D Customer Segments', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax, label='Cluster', shrink=0.5)
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Detailed Segment Profiles")
        
        for cluster_id in range(model.n_clusters):
            cluster_data = df[df['Cluster'] == cluster_id]
            
            with st.expander(f"Cluster {cluster_id}: {cluster_names[cluster_id]} (n={len(cluster_data)})", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Avg Age", f"{cluster_data['Age'].mean():.1f}")
                with col2:
                    st.metric("Avg Income", f"${cluster_data['Annual Income (k$)'].mean():.1f}k")
                with col3:
                    st.metric("Avg Spending", f"{cluster_data['Spending Score (1-100)'].mean():.1f}")
                with col4:
                    gender_mode = cluster_data['Gender'].mode()[0]
                    st.metric("Primary Gender", gender_mode)
                
                st.write("**Characteristics:**")
                st.write(f"- Age range: {cluster_data['Age'].min()} - {cluster_data['Age'].max()} years")
                st.write(f"- Income range: ${cluster_data['Annual Income (k$)'].min()}k - ${cluster_data['Annual Income (k$)'].max()}k")
                st.write(f"- Spending range: {cluster_data['Spending Score (1-100)'].min()} - {cluster_data['Spending Score (1-100)'].max()}")
                
                gender_dist = cluster_data['Gender'].value_counts().to_dict()
                st.write(f"- Gender distribution: {gender_dist}")
    
    with tab3:
        st.subheader("Model Evaluation Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Silhouette Score", "0.304", help="Measures cluster cohesion (range: -1 to 1, higher is better)")
        with col2:
            st.metric("Davies-Bouldin Index", "1.167", delta="-0.8", delta_color="inverse", 
                     help="Measures cluster separation (lower is better)")
        with col3:
            st.metric("Calinski-Harabasz", "68.96", help="Ratio of between-cluster to within-cluster variance (higher is better)")
        
        st.markdown("---")
        
        st.subheader("Elbow Analysis")
        
        inertias = [588.80, 476.79, 388.72, 331.31, 276.41, 236.20, 199.75, 174.24, 152.03]
        silhouettes = [0.252, 0.260, 0.298, 0.304, 0.331, 0.357, 0.388, 0.403, 0.421]
        K_range = range(2, 11)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
            ax.axvline(x=5, color='red', linestyle='--', alpha=0.7, label='Selected K=5')
            ax.set_xlabel('Number of Clusters (K)')
            ax.set_ylabel('Inertia (WCSS)')
            ax.set_title('Elbow Method')
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(K_range, silhouettes, 'ro-', linewidth=2, markersize=8)
            ax.axvline(x=5, color='blue', linestyle='--', alpha=0.7, label='Selected K=5')
            ax.set_xlabel('Number of Clusters (K)')
            ax.set_ylabel('Silhouette Score')
            ax.set_title('Silhouette Analysis')
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)

elif page == "Prediction Tool":
    st.title("Customer Segment Predictor")
    st.markdown("Enter customer information to predict their segment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age", 18, 70, 35)
        income = st.slider("Annual Income (k$)", 15, 140, 60)
    
    with col2:
        spending = st.slider("Spending Score (1-100)", 1, 100, 50)
        gender = st.selectbox("Gender", ["Female", "Male"])
    
    if st.button("Predict Segment", type="primary"):
        gender_encoded = le.transform([gender])[0]
        
        features = np.array([[age, income, spending, gender_encoded]])
        features_scaled = scaler.transform(features)
        
        prediction = model.predict(features_scaled)[0]
        
        st.success(f"### Customer belongs to: **{cluster_names[prediction]}**")
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("**Input Summary:**")
            st.write(f"- Age: {age} years")
            st.write(f"- Income: ${income}k")
            st.write(f"- Spending Score: {spending}")
            st.write(f"- Gender: {gender}")
        
        with col2:
            cluster_data = df[df['Cluster'] == prediction]
            st.write("**Segment Statistics:**")
            st.write(f"- Avg Age: {cluster_data['Age'].mean():.1f} years")
            st.write(f"- Avg Income: ${cluster_data['Annual Income (k$)'].mean():.1f}k")
            st.write(f"- Avg Spending: {cluster_data['Spending Score (1-100)'].mean():.1f}")
            st.write(f"- Segment Size: {len(cluster_data)} customers")
        
        st.markdown("---")
        
        st.subheader("Customer Position in Segment Space")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scatter = ax.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'],
                           c=df['Cluster'], cmap='viridis', s=50, alpha=0.3, edgecolors='black')
        
        ax.scatter(income, spending, c='red', s=500, alpha=1, marker='*', 
                  edgecolors='black', linewidths=2, label='Your Customer', zorder=5)
        
        ax.set_xlabel('Annual Income (k$)', fontsize=12)
        ax.set_ylabel('Spending Score (1-100)', fontsize=12)
        ax.set_title('Customer Position in Segment Space', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)
        plt.colorbar(scatter, ax=ax, label='Cluster')
        
        st.pyplot(fig)

st.sidebar.markdown("---")
st.sidebar.info("**Customer Segmentation Dashboard**\n\nBuilt with K-Means clustering for targeted marketing strategies.")
