"""Run the music recommender in the terminal."""

from textwrap import wrap

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
        title_width = max([len("Song Title")] + [len(song["title"]) for song, _, _ in recommendations])
        header = f"{'Rank':>4} | {'Song Title':<{title_width}} | {'Score':>5} | "
        print(header + "Reasons")
        print("-" * (len(header) + 43))
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            lines = wrap(explanation, width=43, subsequent_indent="  ",
                         break_long_words=False, break_on_hyphens=False)
            print(f"{rank:>4} | {song['title']:<{title_width}} | {score:>5.2f} | {lines[0]}")
            for line in lines[1:]:
                print(f"{'':>4} | {'':<{title_width}} | {'':>5} | {line}")
        print()


if __name__ == "__main__":
    main()
