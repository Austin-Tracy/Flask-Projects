import numpy as np
import matplotlib.pyplot as plt

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculates the Euclidean distance between two points.

    Args:
        a (numpy.ndarray): The first point.
        b (numpy.ndarray): The second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return np.sqrt(np.sum((a - b)**2))

class KMeans:
    def __init__(self, K: int = 4, max_iters: int = 100, plot_steps: bool = False) -> None:
        """
        Initializes a KMeans object.

        Args:
            K (int, optional): The number of clusters. Defaults to 4.
            max_iters (int, optional): The maximum number of iterations. Defaults to 100.
            plot_steps (bool, optional): Whether to plot the clustering steps. Defaults to False.
        """
        self.K = K
        self.max_iters = max_iters
        self.plot_steps = plot_steps
        self.clusters = [[] for _ in range(self.K)]
        self.centroids = []

    def train(self, X: np.ndarray) -> np.ndarray:
        """
        Trains the KMeans model on the given data.

        Args:
            X (numpy.ndarray): The data to train the model on.

        Returns:
            numpy.ndarray: The cluster labels for each data point.
        """
        self.X = X
        self.n_samples, self.n_features = X.shape

        random_sample_idxs = np.random.choice(self.n_samples, self.K, replace=False)
        self.centroids = [self.X[idx] for idx in random_sample_idxs]

        for _ in range(self.max_iters):
            self.clusters = self._create_clusters(self.centroids)
            if self.plot_steps: self.plot()
            centroids_old = self.centroids
            self.centroids = self._get_centroids(self.clusters)

            if self._is_converged(centroids_old, self.centroids):
                break

        return self._get_cluster_labels(self.clusters)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the cluster labels for the given data.

        Args:
            X (numpy.ndarray): The data to predict the cluster labels for.

        Returns:
            numpy.ndarray: The cluster labels for each data point.
        """
        self.X = X
        self.n_samples, self.n_features = X.shape
        clusters = self._create_clusters(self.centroids)
        return self._get_cluster_labels(clusters)

    def load_centroids(self, centroids: list) -> None:
        """
        Loads the given centroids into the model.

        Args:
            centroids (list): The centroids to load.
        """
        self.centroids = centroids

    def _get_cluster_labels(self, clusters: list) -> np.ndarray:
        """
        Returns the cluster labels for each data point.

        Args:
            clusters (list): The clusters to get the labels for.

        Returns:
            numpy.ndarray: The cluster labels for each data point.
        """
        labels = np.empty(self.n_samples)

        for cluster_idx, cluster in enumerate(clusters):
            for sample_index in cluster:
                labels[sample_index] = cluster_idx
        return labels

    def _create_clusters(self, centroids: list) -> list:
        """
        Creates clusters based on the given centroids.

        Args:
            centroids (list): The centroids to create the clusters from.

        Returns:
            list: The clusters.
        """
        clusters = [[] for _ in range(self.K)]
        for idx, sample in enumerate(self.X):
            centroid_idx = self._closest_centroid(sample, centroids)
            clusters[centroid_idx].append(idx)
        return clusters

    def _closest_centroid(self, sample: np.ndarray, centroids: list) -> int:
        """
        Returns the index of the closest centroid to the given sample.

        Args:
            sample (numpy.ndarray): The sample to find the closest centroid to.
            centroids (list): The centroids to choose from.

        Returns:
            int: The index of the closest centroid.
        """
        distances = [euclidean_distance(sample, point) for point in centroids]
        closest_index = np.argmin(distances)
        return closest_index

    def _get_centroids(self, clusters: list) -> np.ndarray:
        """
        Returns the centroids for the given clusters.

        Args:
            clusters (list): The clusters to get the centroids for.

        Returns:
            numpy.ndarray: The centroids.
        """
        centroids = np.zeros((self.K, self.n_features))
        for cluster_idx, cluster in enumerate(clusters):
            cluster_mean = np.mean(self.X[cluster], axis=0)
            centroids[cluster_idx] = cluster_mean
        return centroids

    def _is_converged(self, centroids_old: list, centroids: list) -> bool:
        """
        Checks if the centroids have converged.

        Args:
            centroids_old (list): The old centroids.
            centroids (list): The new centroids.

        Returns:
            bool: Whether the centroids have converged.
        """
        distances = [euclidean_distance(centroids_old[i], centroids[i]) for i in range(self.K)]
        return sum(distances) == 0

    def calculate_WCSS(self) -> float:
        """
        Calculates the Within-Cluster Sum of Squares (WCSS) for the current clustering.

        Returns:
            float: The WCSS.
        """
        WCSS = 0
        for idx, cluster in enumerate(self.clusters):
            centroid = self.centroids[idx]
            wcss_cluster = np.sum((self.X[cluster] - centroid) ** 2)
            WCSS += wcss_cluster
        return WCSS

    def elbow_method(self, max_clusters: int) -> None:
        """
        Plots the Within-Cluster Sum of Squares (WCSS) for different numbers of clusters to help determine the optimal number of clusters.

        Args:
            max_clusters (int): The maximum number of clusters to consider.
        """
        wcss_values = []
        for i in range(1, max_clusters+1):
            self.K = i
            self.predict(self.X)
            wcss_values.append(self.calculate_WCSS())
        plt.plot(range(1, max_clusters+1), wcss_values)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()

    def scatterplot(self) -> None:
        """
        Plots a scatterplot of the data with the clusters and centroids.
        """
        # Since we can't plot n-dimensional data, we plot the first two features for simplicity.
        plt.figure(figsize=(10, 7))
        for idx, cluster in enumerate(self.clusters):
            samples = self.X[cluster]
            plt.scatter(samples[:, 0], samples[:, 1], label=f'Cluster {idx}')
        for idx, centroid in enumerate(self.centroids):
            plt.scatter(centroid[0], centroid[1], marker='x', color='black', s=130)
        plt.legend()
        plt.show()