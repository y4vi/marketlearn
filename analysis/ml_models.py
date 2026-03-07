from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def volatility_clustering(data, n_clusters=3):
    """
    Perform KMeans clustering on stock volatility data.

    Parameters:
    data (DataFrame): DataFrame containing stock volatility features.
    n_clusters (int): Number of clusters for KMeans.

    Returns:
    DataFrame: Original DataFrame with an additional 'Cluster' column.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['Cluster'] = kmeans.fit_predict(scaled_data)

    return data