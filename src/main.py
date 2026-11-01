"""Run the music recommender in the terminal."""

from .recommender import load_songs, recommend_songs


def main() -> None:
    """Load the catalog and print five recommendations for the default profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    print(f"Profile: Happy Pop {user_prefs}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
