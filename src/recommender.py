import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict, dataclass

@dataclass
class Song:
    """Store a song and all its CSV attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """Store a user's music preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """Recommend Song objects using the shared scoring functions."""
    def __init__(self, songs: List[Song]):
        """Store the song catalog."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Rank songs with the shared scoring rule and return the original objects."""
        results = recommend_songs(_user_preferences(user), [asdict(song) for song in self.songs], k)
        songs_by_id = {song.id: song for song in self.songs}
        return [songs_by_id[song["id"]] for song, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a song using the shared scoring rule."""
        _, reasons = score_song(_user_preferences(user), asdict(song))
        return "; ".join(reasons)

def _user_preferences(user: UserProfile) -> Dict:
    """Map the class profile to the baseline preference dictionary."""
    return {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}

def load_songs(csv_path: str) -> List[Dict]:
    """Load all CSV columns, converting IDs and numerical features to numbers."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for song in csv.DictReader(csv_file):
            song["id"] = int(song["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                song[field] = float(song[field])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score genre, mood, and energy matches and explain their points."""
    genre_match = song["genre"] == user_prefs["genre"]
    mood_match = song["mood"] == user_prefs["mood"]
    energy_gap = abs(song["energy"] - user_prefs["energy"])
    energy_similarity = max(0, 1 - energy_gap)
    score = 2.0 * genre_match + 1.0 * mood_match + energy_similarity
    reasons = [
        "genre match (+2.0)" if genre_match else "genre mismatch (+0.0)",
        "mood match (+1.0)" if mood_match else "mood mismatch (+0.0)",
        f"energy gap {energy_gap:.2f}, similarity {energy_similarity:.2f} (+{energy_similarity:.2f})",
    ]
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return up to k songs by score, breaking ties by ascending numeric ID."""
    if k <= 0:
        return []
    results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        results.append((song, score, "; ".join(reasons)))
    return sorted(results, key=lambda result: (-result[1], int(result[0]["id"])))[:k]
