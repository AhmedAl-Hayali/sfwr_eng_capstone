import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class Recommendation:
    def __init__(self, data=None, file_path=None):
        """
        Initialize the Recommendation system.
        
        Parameters:
            data (pd.DataFrame): Optional dataframe for testing.
            file_path (str): Path to the CSV file (only used if data is not provided).
        """
        if data is not None:
            self.df = data  # Directly use provided DataFrame
        elif file_path:
            self.df = pd.read_csv(file_path)  # Load from CSV file
        else:
            raise ValueError("Must provide either 'data' or 'file_path'.")

        self.df_encoded = self.df.copy()

        # Convert categorical features (major/minor) to numerical
        self.df_encoded['keymjr'] = self.df_encoded['keymjr'].astype('category').cat.codes
        self.df_encoded['keymnr'] = self.df_encoded['keymnr'].astype('category').cat.codes

        # Select numerical feature columns (excluding 'track_name')
        self.feature_cols = [col for col in self.df_encoded.columns if col not in ['track_name']]
        self.features = self.df_encoded[self.feature_cols]

        # Normalize data
        self.scaler = StandardScaler()
        self.features_scaled = self.scaler.fit_transform(self.features)

        # Compute similarity matrix
        self.similarity_matrix = cosine_similarity(self.features_scaled)
        self.similarity_df = pd.DataFrame(self.similarity_matrix, index=self.df['track_name'], columns=self.df['track_name'])

    def get_similar_songs(self, reference_track, top_n=10):
        """Retrieve top N most similar songs."""
        if reference_track not in self.similarity_df.index:
            return f"Track '{reference_track}' not found in dataset."
        
        similar_tracks = self.similarity_df[reference_track].sort_values(ascending=False)
        return similar_tracks.iloc[1:top_n+1]  # Exclude reference track itself


# def main(reference_song):
#     rec = Recommendation(file_path="src/featurizer/test.csv")
#     our_recs = rec.get_similar_songs(reference_song)
#     print(our_recs)

#     # track_names = our_recs.index.to_numpy()
#     # scores = our_recs.values
#     # print(track_names)
#     # print(scores)

# if __name__ == "__main__":
#     main("Serenata")
