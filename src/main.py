"""Run the music recommender in the terminal."""

from .recommender import load_songs, recommend_songs


def main() -> None:
    """Print five baseline recommendations for each of four taste profiles."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.8}),
        ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.35}),
        ("Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.9}),
        ("Conflicting Preferences", {"genre": "pop", "mood": "sad", "energy": 0.9}),
    ]

    for label, user_prefs in profiles:
        print(f"Profile: {label} {user_prefs}")
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
