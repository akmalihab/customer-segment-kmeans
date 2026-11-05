import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import pickle
import warnings
from config import *

warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv(MALL_CUSTOMERS_CSV)

print("="*60)
print("DESCRIPTIVE STATISTICS")
print("="*60)

# Basic info
print(f"\nDataset Shape: {df.shape}")
print(f"\nColumn Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nDuplicate Rows: {df.duplicated().sum()}")

# Statistical summary
print("\nNumerical Statistics:")
print(df.describe())

print("\nCategorical Distribution:")
print(df['Gender'].value_counts())

print("\n" + "="*60)
print("EXPLORATORY DATA ANALYSIS")
print("="*60)

# Age distribution by gender
print("\nAge by Gender:")
print(df.groupby('Gender')['Age'].describe())

print("\nIncome by Gender:")
print(df.groupby('Gender')['Annual Income (k$)'].describe())

print("\nSpending Score by Gender:")
print(df.groupby('Gender')['Spending Score (1-100)'].describe())

# Correlation
print("\nCorrelation Matrix:")
print(df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].corr())

# Visualizations
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Age distribution
axes[0, 0].hist(df['Age'], bins=20, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Age Distribution')
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Frequency')

# Income distribution
axes[0, 1].hist(df['Annual Income (k$)'], bins=20, color='lightgreen', edgecolor='black')
axes[0, 1].set_title('Annual Income Distribution')
axes[0, 1].set_xlabel('Income (k$)')
axes[0, 1].set_ylabel('Frequency')

# Spending score distribution
axes[0, 2].hist(df['Spending Score (1-100)'], bins=20, color='salmon', edgecolor='black')
axes[0, 2].set_title('Spending Score Distribution')
axes[0, 2].set_xlabel('Spending Score')
axes[0, 2].set_ylabel('Frequency')

# Gender distribution
gender_counts = df['Gender'].value_counts()
axes[1, 0].bar(gender_counts.index, gender_counts.values, color=['lightblue', 'pink'])
axes[1, 0].set_title('Gender Distribution')
axes[1, 0].set_xlabel('Gender')
axes[1, 0].set_ylabel('Count')

# Income vs Spending
axes[1, 1].scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], 
                   c=df['Age'], cmap='viridis', alpha=0.6)
axes[1, 1].set_title('Income vs Spending Score')
axes[1, 1].set_xlabel('Income (k$)')
axes[1, 1].set_ylabel('Spending Score')
cbar = plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1])
cbar.set_label('Age')

# Box plot - Age by Gender
df.boxplot(column='Age', by='Gender', ax=axes[1, 2])
axes[1, 2].set_title('Age by Gender')
axes[1, 2].set_xlabel('Gender')
axes[1, 2].set_ylabel('Age')

plt.tight_layout()
plt.savefig(EDA_VISUALIZATION_PNG, dpi=300, bbox_inches='tight')
print(f"\nEDA visualization saved: {EDA_VISUALIZATION_PNG}")

# Correlation heatmap
plt.figure(figsize=(8, 6))
corr_matrix = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig(CORRELATION_HEATMAP_PNG, dpi=300, bbox_inches='tight')
print(f"Correlation heatmap saved: {CORRELATION_HEATMAP_PNG}")

print("\n" + "="*60)
print("DATA PREPROCESSING")
print("="*60)

# Drop CustomerID (not useful for clustering)
df_processed = df.drop('CustomerID', axis=1)

# Encode Gender
le = LabelEncoder()
df_processed['Gender_Encoded'] = le.fit_transform(df_processed['Gender'])

# Features for clustering
feature_cols = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)', 'Gender_Encoded']
X = df_processed[feature_cols].copy()

print(f"\nFeatures selected: {feature_cols}")
print(f"Feature matrix shape: {X.shape}")

# Check for outliers using IQR method
print("\nOutlier Detection (IQR method):")
for col in X.columns:
    Q1 = X[col].quantile(0.25)
    Q3 = X[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((X[col] < (Q1 - 1.5 * IQR)) | (X[col] > (Q3 + 1.5 * IQR))).sum()
    print(f"  {col}: {outliers} outliers")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)

print("\nScaled Features Statistics:")
print(X_scaled_df.describe())

print("\n" + "="*60)
print("K-MEANS CLUSTERING")
print("="*60)

# Elbow method to find optimal k
inertias = []
silhouette_scores = []
K_range = range(2, 11)

print("\nElbow Method & Silhouette Analysis:")
for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette Score={silhouette_scores[-1]:.3f}")

# Plot elbow curve
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('Number of Clusters (K)')
ax1.set_ylabel('Inertia (WCSS)')
ax1.set_title('Elbow Method')
ax1.grid(True, alpha=0.3)

ax2.plot(K_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
ax2.set_xlabel('Number of Clusters (K)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score by K')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(ELBOW_SILHOUETTE_PNG, dpi=300, bbox_inches='tight')
print(f"\nElbow & Silhouette plot saved: {ELBOW_SILHOUETTE_PNG}")

# Based on elbow/silhouette, choose optimal k (typically 5 for this dataset)
optimal_k = 5
print(f"\nOptimal K selected: {optimal_k}")

# Train final model
kmeans_final = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42, n_init=10)
clusters = kmeans_final.fit_predict(X_scaled)

# Add cluster labels to dataframe
df_processed['Cluster'] = clusters

print("\n" + "="*60)
print("MODEL EVALUATION")
print("="*60)

# Evaluation metrics
silhouette = silhouette_score(X_scaled, clusters)
davies_bouldin = davies_bouldin_score(X_scaled, clusters)
calinski_harabasz = calinski_harabasz_score(X_scaled, clusters)

print(f"\nSilhouette Score: {silhouette:.4f}")
print(f"Davies-Bouldin Index: {davies_bouldin:.4f} (lower is better)")
print(f"Calinski-Harabasz Index: {calinski_harabasz:.4f} (higher is better)")

# Cluster distribution
print("\nCluster Distribution:")
print(df_processed['Cluster'].value_counts().sort_index())

# Cluster characteristics
print("\nCluster Characteristics:")
cluster_summary = df_processed.groupby('Cluster')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
print(cluster_summary)

# Visualize clusters
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Income vs Spending Score
scatter1 = axes[0].scatter(df_processed['Annual Income (k$)'], 
                           df_processed['Spending Score (1-100)'],
                           c=df_processed['Cluster'], cmap='viridis', 
                           s=50, alpha=0.6, edgecolors='black')
axes[0].scatter(kmeans_final.cluster_centers_[:, 1] * scaler.scale_[1] + scaler.mean_[1],
                kmeans_final.cluster_centers_[:, 2] * scaler.scale_[2] + scaler.mean_[2],
                c='red', s=300, alpha=0.8, marker='X', edgecolors='black', linewidths=2,
                label='Centroids')
axes[0].set_xlabel('Annual Income (k$)')
axes[0].set_ylabel('Spending Score (1-100)')
axes[0].set_title('Customer Segments (Income vs Spending)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
plt.colorbar(scatter1, ax=axes[0], label='Cluster')

# Age vs Spending Score
scatter2 = axes[1].scatter(df_processed['Age'], 
                           df_processed['Spending Score (1-100)'],
                           c=df_processed['Cluster'], cmap='viridis', 
                           s=50, alpha=0.6, edgecolors='black')
axes[1].scatter(kmeans_final.cluster_centers_[:, 0] * scaler.scale_[0] + scaler.mean_[0],
                kmeans_final.cluster_centers_[:, 2] * scaler.scale_[2] + scaler.mean_[2],
                c='red', s=300, alpha=0.8, marker='X', edgecolors='black', linewidths=2,
                label='Centroids')
axes[1].set_xlabel('Age')
axes[1].set_ylabel('Spending Score (1-100)')
axes[1].set_title('Customer Segments (Age vs Spending)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.colorbar(scatter2, ax=axes[1], label='Cluster')

plt.tight_layout()
plt.savefig(CLUSTER_VISUALIZATION_PNG, dpi=300, bbox_inches='tight')
print(f"\nCluster visualization saved: {CLUSTER_VISUALIZATION_PNG}")

# 3D visualization
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(df_processed['Age'], 
                     df_processed['Annual Income (k$)'],
                     df_processed['Spending Score (1-100)'],
                     c=df_processed['Cluster'], cmap='viridis',
                     s=50, alpha=0.6, edgecolors='black')

ax.set_xlabel('Age')
ax.set_ylabel('Annual Income (k$)')
ax.set_zlabel('Spending Score (1-100)')
ax.set_title('3D Customer Segments')
plt.colorbar(scatter, ax=ax, label='Cluster', shrink=0.5)

plt.savefig(CLUSTER_3D_PNG, dpi=300, bbox_inches='tight')
print(f"3D cluster visualization saved: {CLUSTER_3D_PNG}")

# Save model and artifacts
with open(KMEANS_MODEL_PKL, 'wb') as f:
    pickle.dump(kmeans_final, f)
print(f"\nModel saved: {KMEANS_MODEL_PKL}")

with open(SCALER_PKL, 'wb') as f:
    pickle.dump(scaler, f)
print(f"Scaler saved: {SCALER_PKL}")

with open(LABEL_ENCODER_PKL, 'wb') as f:
    pickle.dump(le, f)
print(f"Label encoder saved: {LABEL_ENCODER_PKL}")

df_processed.to_csv(CUSTOMER_SEGMENTS_CSV, index=False)
print(f"Segmented data saved: {CUSTOMER_SEGMENTS_CSV}")

# Cluster profiles
print("\n" + "="*60)
print("CLUSTER PROFILES")
print("="*60)

for cluster_id in range(optimal_k):
    cluster_data = df_processed[df_processed['Cluster'] == cluster_id]
    print(f"\nCluster {cluster_id} (n={len(cluster_data)}):")
    print(f"  Age: {cluster_data['Age'].mean():.1f} ± {cluster_data['Age'].std():.1f}")
    print(f"  Income: ${cluster_data['Annual Income (k$)'].mean():.1f}k ± ${cluster_data['Annual Income (k$)'].std():.1f}k")
    print(f"  Spending: {cluster_data['Spending Score (1-100)'].mean():.1f} ± {cluster_data['Spending Score (1-100)'].std():.1f}")
    print(f"  Gender: {cluster_data['Gender'].mode()[0]} ({cluster_data['Gender'].value_counts().to_dict()})")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
