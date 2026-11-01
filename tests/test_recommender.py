from src.recommender import Song, UserProfile, Recommender
from src.recommender import recommend_songs, score_song
from copy import deepcopy
from dataclasses import asdict

import pytest

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


DEFAULT_PREFS = {"genre": "pop", "mood": "happy", "energy": 0.8}


def make_song_dict(song_id=1, **changes):
    song = asdict(make_small_recommender().songs[0])
    song["id"] = song_id
    song.update(changes)
    return song


def test_known_score_and_reasons():
    score, reasons = score_song(DEFAULT_PREFS, make_song_dict(energy=0.82))

    assert score == pytest.approx(3.98)
    assert reasons == [
        "genre match (+2.0)",
        "mood match (+1.0)",
        "energy gap 0.02, similarity 0.98 (+0.98)",
    ]


@pytest.mark.parametrize("genre,mood,energy,expected", [
    ("pop", "happy", 0.8, 4.0),
    ("lofi", "chill", 0.8, 1.0),
    ("pop", "chill", 0.8, 3.0),
    ("lofi", "happy", 0.8, 2.0),
    ("Pop", "Happy", 0.8, 1.0),
    ("pop", "happy", 2.8, 3.0),
])
def test_score_uses_exact_matches_and_clamped_energy(genre, mood, energy, expected):
    song = make_song_dict(genre=genre, mood=mood, energy=energy)
    score, reasons = score_song(DEFAULT_PREFS, song)

    assert score == pytest.approx(expected)
    assert reasons[0] == ("genre match (+2.0)" if genre == "pop" else "genre mismatch (+0.0)")
    assert reasons[1] == ("mood match (+1.0)" if mood == "happy" else "mood mismatch (+0.0)")
    if energy == 2.8:
        assert reasons[2] == "energy gap 2.00, similarity 0.00 (+0.00)"


def test_closer_energy_beats_higher_energy():
    closer, _ = score_song(DEFAULT_PREFS, make_song_dict(energy=0.7))
    higher, _ = score_song(DEFAULT_PREFS, make_song_dict(energy=1.0))

    assert closer == pytest.approx(3.9)
    assert higher == pytest.approx(3.8)
    assert closer > higher


def test_rank_unsorted_catalog_without_mutating_it():
    songs = [
        make_song_dict(1, genre="lofi", mood="chill", energy=0.4),
        make_song_dict(3, mood="chill"),
        make_song_dict(2),
    ]
    original = deepcopy(songs)

    results = recommend_songs(DEFAULT_PREFS, songs, k=3)

    assert [song["id"] for song, _, _ in results] == [2, 3, 1]
    assert [score for _, score, _ in results] == pytest.approx([4.0, 3.0, 0.6])
    assert songs == original
    assert results[0][0] is songs[2]
    assert results[0][2] == (
        "genre match (+2.0); mood match (+1.0); "
        "energy gap 0.00, similarity 1.00 (+1.00)"
    )


def test_ties_use_numeric_ids():
    songs = [make_song_dict(song_id) for song_id in ("10", "2", "1")]

    results = recommend_songs(DEFAULT_PREFS, songs)

    assert [song["id"] for song, _, _ in results] == ["1", "2", "10"]


def test_ranking_keeps_unrounded_scores():
    songs = [make_song_dict(1, energy=0.802), make_song_dict(10, energy=0.801)]

    results = recommend_songs(DEFAULT_PREFS, songs)

    assert [song["id"] for song, _, _ in results] == [10, 1]
    assert results[0][1] > results[1][1]
    assert f"{results[0][1]:.2f}" == f"{results[1][1]:.2f}"


@pytest.mark.parametrize("k,expected_ids", [
    (-1, []), (0, []), (1, [1]), (2, [1, 2]), (10, [1, 2]),
])
def test_recommendation_k_boundaries(k, expected_ids):
    songs = [make_song_dict(2), make_song_dict(1)]

    assert [song["id"] for song, _, _ in recommend_songs(DEFAULT_PREFS, songs, k)] == expected_ids


def test_empty_catalog():
    assert recommend_songs(DEFAULT_PREFS, []) == []
    user = UserProfile("pop", "happy", 0.8, False)
    assert Recommender([]).recommend(user) == []


@pytest.mark.parametrize("likes_acoustic", [False, True])
def test_class_and_function_order_and_explanations_agree(likes_acoustic):
    catalog = [
        make_song_dict(10),
        make_song_dict(3, genre="lofi", mood="chill", energy=0.4),
        make_song_dict(2),
    ]
    songs = [Song(**song) for song in catalog]
    rec = Recommender(songs)
    user = UserProfile("pop", "happy", 0.8, likes_acoustic)

    functional = recommend_songs(DEFAULT_PREFS, catalog)
    ranked = rec.recommend(user)

    assert [song.id for song in ranked] == [2, 10, 3]
    assert [song.id for song in ranked] == [song["id"] for song, _, _ in functional]
    assert ranked[0] is songs[2]
    assert rec.songs == songs
    for song, (_, _, explanation) in zip(ranked, functional):
        assert rec.explain_recommendation(user, song) == explanation
    assert rec.recommend(user, k=1) == [songs[2]]
    assert rec.recommend(user, k=0) == []
    assert rec.recommend(user, k=-1) == []
