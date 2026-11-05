# Customer Segmentation Analysis - K-Means Clustering

## Project Overview

Customer segmentation project using K-Means clustering on Mall Customer dataset. Identifies distinct customer groups for targeted marketing strategies.

**Key Technologies:** Python, scikit-learn, Streamlit, pandas, matplotlib, seaborn

## Dataset

**Source:** `Mall_Customers.csv`

**Shape:** 200 customers × 5 features

**Features:**
- `CustomerID`: Unique identifier
- `Gender`: Male/Female
- `Age`: 18-70 years
- `Annual Income (k$)`: 15-137k
- `Spending Score (1-100)`: 1-99

**Data Quality:**
- No missing values
- No duplicates
- 2 outliers in Annual Income (retained)

## Descriptive Statistics

| Metric | Age | Income (k$) | Spending Score |
|--------|-----|-------------|----------------|
| Mean | 38.85 | 60.56 | 50.20 |
| Std | 13.97 | 26.26 | 25.82 |
| Min | 18 | 15 | 1 |
| Max | 70 | 137 | 99 |

**Gender Distribution:**
- Female: 112 (56%)
- Male: 88 (44%)

## Exploratory Data Analysis

### Key Findings

1. **Age Distribution**
   - Bimodal distribution with peaks around 30 and 50 years
   - Mean age: 38.85 years
   - No significant difference between genders

2. **Income Distribution**
   - Approximately normal distribution
   - Slight right skew
   - Males: $62.2k average, Females: $59.3k average

3. **Spending Score Distribution**
   - Uniform distribution across range
   - Females: 51.5 average, Males: 48.5 average

4. **Correlations**
   - Age vs Income: -0.012 (no correlation)
   - Age vs Spending: -0.327 (negative - younger customers spend more)
   - Income vs Spending: 0.010 (no correlation - spending independent of income)

### Visualizations Generated
- `eda_visualization.png` - Distribution plots and scatter plots
- `correlation_heatmap.png` - Feature correlation matrix

## Data Preprocessing

### Steps

1. **Feature Engineering**
   - Dropped `CustomerID` (not predictive)
   - Encoded `Gender` using LabelEncoder (Female=0, Male=1)

2. **Feature Selection**
   - Selected 4 features: Age, Income, Spending Score, Gender_Encoded

3. **Outlier Detection**
   - IQR method applied
   - 2 outliers detected in Income (retained for real-world representation)

4. **Standardization**
   - StandardScaler applied to all features
   - Mean=0, Std=1 for each feature
   - Critical for distance-based K-Means algorithm

## Model Development

### Algorithm: K-Means Clustering

**Hyperparameters:**
- `init='k-means++'` - Smart centroid initialization
- `n_init=10` - Run algorithm 10 times
- `random_state=42` - Reproducibility

### Optimal K Selection

**Elbow Method:**
- Tested K=2 to K=10
- Elbow observed around K=5-6
- Selected K=5 for interpretability

**Silhouette Analysis:**
| K | Inertia | Silhouette Score |
|---|---------|------------------|
| 2 | 588.80 | 0.252 |
| 3 | 476.79 | 0.260 |
| 4 | 388.72 | 0.298 |
| **5** | **331.31** | **0.304** |
| 6 | 276.41 | 0.331 |
| 7 | 236.20 | 0.357 |

**Decision:** K=5 selected (balance between elbow point and business interpretability)

## Model Evaluation

### Clustering Metrics

| Metric | Score | Interpretation |
|--------|-------|----------------|
| **Silhouette Score** | 0.3041 | Moderate cluster quality (0.2-0.5 range) |
| **Davies-Bouldin Index** | 1.1672 | Good separation (lower is better) |
| **Calinski-Harabasz Index** | 68.9646 | Reasonable cluster definition (higher is better) |

### Cluster Distribution

| Cluster | Count | % |
|---------|-------|---|
| 0 | 39 | 19.5% |
| 1 | 29 | 14.5% |
| 2 | 43 | 21.5% |
| 3 | 54 | 27.0% |
| 4 | 35 | 17.5% |

## Customer Segments

### Cluster 0: High Income, High Spenders (n=39)
- **Age:** 32.7 ± 3.7 years (young adults)
- **Income:** $86.5k ± $16.3k (high)
- **Spending:** 82.1 ± 9.4 (very high)
- **Gender:** Balanced (54% Female, 46% Male)
- **Strategy:** Premium products, luxury offerings, VIP programs

### Cluster 1: High Income, Low Spenders (n=29)
- **Age:** 36.5 ± 9.7 years (adults)
- **Income:** $89.5k ± $17.4k (highest)
- **Spending:** 18.0 ± 10.6 (very low)
- **Gender:** Balanced (55% Female, 45% Male)
- **Strategy:** Value propositions, investment products, quality over quantity messaging

### Cluster 2: Middle Age, Average (n=43)
- **Age:** 49.8 ± 9.5 years (middle-aged)
- **Income:** $49.2k ± $15.6k (moderate)
- **Spending:** 40.1 ± 15.6 (moderate)
- **Gender:** 100% Female
- **Strategy:** Family-oriented products, practical offers, loyalty programs

### Cluster 3: Young, Moderate Spenders (n=54)
- **Age:** 24.9 ± 5.3 years (young)
- **Income:** $39.7k ± $17.0k (low-moderate)
- **Spending:** 61.2 ± 18.4 (moderate-high)
- **Gender:** 59% Female, 41% Male
- **Strategy:** Trendy products, social media marketing, flexible payment options

### Cluster 4: Older, Conservative (n=35)
- **Age:** 55.7 ± 9.6 years (older)
- **Income:** $53.7k ± $18.7k (moderate)
- **Spending:** 36.8 ± 18.0 (low-moderate)
- **Gender:** 100% Male
- **Strategy:** Traditional marketing, reliability focus, senior discounts

## Visualizations

### Generated Plots
1. `elbow_silhouette.png` - K selection analysis
2. `cluster_visualization.png` - 2D scatter plots with centroids
3. `cluster_3d.png` - 3D visualization of all features

## Dashboard Implementation

### Streamlit Dashboard Features

**Run command:** `streamlit run dashboard.py`

#### Pages

1. **Overview**
   - Key metrics (total customers, clusters, features)
   - Dataset preview
   - Statistical summary
   - Cluster distribution chart

2. **Data Analysis**
   - Feature distributions (histograms)
   - Correlation heatmap
   - Gender comparisons
   - Box plots

3. **Clustering Results**
   - 2D scatter plots (Income vs Spending, Age vs Spending)
   - 3D interactive visualization
   - Detailed segment profiles with expandable cards
   - Model evaluation metrics
   - Elbow analysis charts

4. **Prediction Tool**
   - Interactive sliders for customer attributes
   - Real-time segment prediction
   - Customer positioning visualization
   - Comparison with segment statistics

### Interactive Features
- Multi-page navigation
- Expandable segment profiles
- Dynamic visualizations
- Real-time prediction

## Files Generated

### Scripts
- `analysis.py` - Complete analysis pipeline
- `dashboard.py` - Streamlit dashboard application

### Models & Artifacts
- `kmeans_model.pkl` - Trained K-Means model
- `scaler.pkl` - StandardScaler for preprocessing
- `label_encoder.pkl` - Gender encoder

### Data
- `customer_segments.csv` - Original data with cluster labels

### Visualizations
- `eda_visualization.png` - EDA plots
- `correlation_heatmap.png` - Correlation matrix
- `elbow_silhouette.png` - K selection plots
- `cluster_visualization.png` - 2D cluster plots
- `cluster_3d.png` - 3D cluster plot

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execute Analysis
```bash
python src/analysis.py
```

Generates all visualizations, models, and evaluation metrics automatically.

### Interactive Notebook
```bash
jupyter notebook notebooks/customer_segmentation_analysis.ipynb
```

Step-by-step analysis with detailed explanations and visualizations.

### Launch Dashboard
```bash
streamlit run dashboard.py
```

Opens interactive dashboard at `http://localhost:8501`

## Business Insights

### Marketing Recommendations

1. **Cluster 0 (High Income, High Spenders)**
   - Premium tier customers
   - Target with luxury products and exclusive events
   - High ROI potential

2. **Cluster 1 (High Income, Low Spenders)**
   - Untapped potential
   - Focus on value demonstration
   - Convert to high spenders through targeted campaigns

3. **Cluster 2 (Middle Age, Average)**
   - Stable customer base
   - Family-oriented promotions
   - Loyalty rewards to increase retention

4. **Cluster 3 (Young, Moderate Spenders)**
   - Growing segment
   - Digital-first approach
   - Build brand loyalty early

5. **Cluster 4 (Older, Conservative)**
   - Traditional approach needed
   - Focus on quality and reliability
   - Lower acquisition cost strategy

### Key Takeaways

- **5 distinct customer segments** identified with clear characteristics
- **Income doesn't predict spending** - psychological factors matter
- **Age influences spending** - younger customers more willing to spend
- **Gender differences in segments** - Clusters 2 and 4 gender-specific
- **Actionable insights** for targeted marketing strategies

## Model Limitations

1. **Feature limitations** - Only 4 features, could benefit from:
   - Purchase history
   - Product preferences
   - Visit frequency
   - Online vs in-store behavior

2. **Temporal aspects** - No time dimension:
   - Seasonal patterns
   - Trend changes
   - Customer lifecycle

3. **Segment overlap** - Moderate silhouette score indicates some overlap between segments

4. **Static segmentation** - Customers may move between segments over time

## Future Improvements

1. **Additional features** - Incorporate behavioral and transactional data
2. **Hierarchical clustering** - Explore sub-segments within main clusters
3. **Time-series analysis** - Track segment evolution
4. **Predictive modeling** - Forecast customer lifetime value by segment
5. **A/B testing** - Validate marketing strategies per segment
6. **Real-time updates** - Retrain model periodically with new data

## Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scikit-learn>=1.2.0
streamlit>=1.25.0
```

## Project Structure

```
customer-segment-kmeans/
├── data/
│   ├── raw/
│   │   └── Mall_Customers.csv          # Original dataset
│   └── processed/
│       └── customer_segments.csv       # Data with cluster labels
├── models/
│   ├── kmeans_model.pkl               # Trained K-Means model
│   ├── scaler.pkl                     # StandardScaler artifact
│   └── label_encoder.pkl              # LabelEncoder artifact
├── outputs/
│   ├── eda_visualization.png          # EDA plots
│   ├── correlation_heatmap.png        # Correlation matrix
│   ├── elbow_silhouette.png          # K selection plots
│   ├── cluster_visualization.png      # 2D cluster plots
│   └── cluster_3d.png                # 3D cluster plot
├── src/
│   ├── config.py                      # Path configurations
│   └── analysis.py                    # Analysis pipeline script
├── notebooks/
│   └── customer_segmentation_analysis.ipynb  # Interactive analysis notebook
├── dashboard.py                       # Streamlit dashboard
├── README.md                          # Documentation
├── requirements.txt                   # Dependencies
└── .gitignore                         # Git ignore rules
```

## Conclusion

Successfully developed customer segmentation system using K-Means clustering. Identified 5 distinct customer groups with actionable marketing strategies. Dashboard enables business users to explore segments and predict new customer segments in real-time.

**Model Performance:** Moderate to good clustering quality with clear business interpretability.

**Business Value:** Enables targeted marketing, personalized offers, and optimized resource allocation.

---

**Project Date:** November 2026  
**Author:** Customer Analytics Team  
**Status:** Complete
