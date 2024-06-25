import base64
from io import BytesIO

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from DataFetchModule import fetch_data, session

class HeartEventClusterer:
    def __init__(self, session):
        self.session = session

    def fetch_and_process_data(self):
        df = fetch_data(self.session, True)
        df['event_time'] = pd.to_datetime(df['event_time'])
        df['hour_of_day'] = df['event_time'].dt.hour
        return df

    def cluster_events(self, df):
        time_aggregates = df.groupby('hour_of_day').agg({
            'personal_data_id': 'size',
        }).rename(columns={'personal_data_id': 'event_count'})

        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(time_aggregates[['event_count']])

        kmeans = KMeans(n_clusters=3, random_state=42)
        time_aggregates['Cluster'] = kmeans.fit_predict(scaled_features)
        return time_aggregates, kmeans.cluster_centers_

    def get_cluster_info(self):
        df = self.fetch_and_process_data()
        clusters, centers = self.cluster_events(df)
        return clusters.to_dict(), centers.tolist()

    def plot(self):
        # Fetch and process data
        df = self.fetch_and_process_data()

        # Perform clustering
        clusters, _ = self.cluster_events(df)

        # Plotting
        plt.figure(figsize=(10, 5))
        colors = ['red', 'green', 'blue']
        for cluster in sorted(clusters['Cluster'].unique()):
            clustered_data = clusters[clusters['Cluster'] == cluster]
            plt.scatter(clustered_data.index, clustered_data['event_count'], color=colors[cluster],
                        label=f'Cluster {cluster}', s=50)

        plt.title('Temporal Clustering of Heart Events')
        plt.xlabel('Hour of Day')
        plt.ylabel('Event Count')
        plt.legend()
        plt.grid(True)

        # Save plot to a bytes buffer
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        # Encode the image in base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return image_base64


if __name__ == '__main__':
    clusterer = HeartEventClusterer(session)
    clusters, centers = clusterer.get_cluster_info()
    print(clusters)
    print(centers)