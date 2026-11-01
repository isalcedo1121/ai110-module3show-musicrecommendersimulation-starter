# 🎵 Music Recommender Simulation

## Project Summary

This project uses 18 fictional songs to suggest music based on genre, mood,
and energy. The Python CLI shows the top five songs and explains their scores.

---

## How The System Works

Collaborative filtering uses patterns in other listeners' likes, skips, and
playlists. Content-based filtering compares song features, like genre, mood,
energy, and tempo, with user preferences.

This project uses content-based filtering because it has a fixed CSV and no
listening histories. The weights are hand-written, not learned from users.
Loading and scoring the CSV does not train a model.

The loader uses Python's `csv` module and keeps every column in each song
dictionary and `Song` object. It turns `id` into an integer and the other
numbers into floats. Titles and artists identify songs. Genre describes style,
mood describes feeling, and energy describes intensity. Only these last three
features affect scores. Tempo, valence, danceability, and acousticness stay stored
but unused in scoring.

The default preferences are:

```python
{"genre": "pop", "mood": "happy", "energy": 0.8}
```

In `UserProfile`, `favorite_genre` maps to `genre`, `favorite_mood` to `mood`,
and `target_energy` to `energy`. We keep `likes_acoustic` for compatibility
with the tests, but it does not affect scores.

Both the dictionary and class versions use this rule:

```text
genre_match = 1 for an exact genre match, otherwise 0
mood_match = 1 for an exact mood match, otherwise 0
energy_similarity = max(0, 1 - abs(song_energy - target_energy))
score = 2.0 * genre_match + 1.0 * mood_match + energy_similarity
```

A perfect match scores 4.0. Energy closer to the target earns more points;
higher energy is not always better. For example, "Sunrise City" is pop, happy,
and has energy 0.82. With the default profile, its score is
`2 + 1 + (1 - abs(0.82 - 0.8)) = 3.98`.

These preferences can tell intense rock from chill lofi if the user asks for
either style. The default happy-pop profile matches neither, so only energy
separates them. The profile misses lyrics, language, favorite artists, and
people who like several styles.

We score every song with reasons, then sort by highest score first without
rounding the scores. Ties use the lowest numeric song ID first. We return the
top `k`; the CLI requests five. Scores are shown to two decimal places.

```text
CSV + preferences -> load and convert numbers -> score all songs with reasons
                  -> sort -> show top five
```

**Prediction to investigate:** Giving genre two points may lead to too many
songs from one genre.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```text
Loaded songs: 18
Profile: High-Energy Pop {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

Top recommendations:

1. Sunrise City - Score: 3.98
Because: genre match (+2.0); mood match (+1.0); energy gap 0.02, similarity 0.98 (+0.98)

2. Gym Hero - Score: 2.87
Because: genre match (+2.0); mood mismatch (+0.0); energy gap 0.13, similarity 0.87 (+0.87)

3. Rooftop Lights - Score: 1.96
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.04, similarity 0.96 (+0.96)

4. Sidewalk Summit - Score: 0.98
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.02, similarity 0.98 (+0.98)

5. Night Drive Loop - Score: 0.95
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.05, similarity 0.95 (+0.95)

Profile: Chill Lofi {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}

Top recommendations:

1. Library Rain - Score: 4.00
Because: genre match (+2.0); mood match (+1.0); energy gap 0.00, similarity 1.00 (+1.00)

2. Midnight Coding - Score: 3.93
Because: genre match (+2.0); mood match (+1.0); energy gap 0.07, similarity 0.93 (+0.93)

3. Focus Flow - Score: 2.95
Because: genre match (+2.0); mood mismatch (+0.0); energy gap 0.05, similarity 0.95 (+0.95)

4. Spacewalk Thoughts - Score: 1.93
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.07, similarity 0.93 (+0.93)

5. Coffee Shop Stories - Score: 0.98
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.02, similarity 0.98 (+0.98)

Profile: Intense Rock {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}

Top recommendations:

1. Storm Runner - Score: 3.99
Because: genre match (+2.0); mood match (+1.0); energy gap 0.01, similarity 0.99 (+0.99)

2. Gym Hero - Score: 1.97
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.03, similarity 0.97 (+0.97)

3. Prism Festival - Score: 0.94
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.06, similarity 0.94 (+0.94)

4. Sunrise City - Score: 0.92
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.08, similarity 0.92 (+0.92)

5. Sidewalk Summit - Score: 0.88
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.12, similarity 0.88 (+0.88)

Profile: Conflicting Preferences {'genre': 'pop', 'mood': 'sad', 'energy': 0.9}

Top recommendations:

1. Gym Hero - Score: 2.97
Because: genre match (+2.0); mood mismatch (+0.0); energy gap 0.03, similarity 0.97 (+0.97)

2. Sunrise City - Score: 2.92
Because: genre match (+2.0); mood mismatch (+0.0); energy gap 0.08, similarity 0.92 (+0.92)

3. Empty Station - Score: 1.48
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.52, similarity 0.48 (+0.48)

4. Winter Window - Score: 1.29
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.71, similarity 0.29 (+0.29)

5. Storm Runner - Score: 0.99
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.01, similarity 0.99 (+0.99)

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Ran four baseline profiles with the same weights: Pop, Lofi, Rock, and
Conflicting Preferences. Then compared genre=2, mood=1, energy=1 with temporary
weights genre=1, mood=1, energy=2. Rooftop Lights moved from third to second for
Pop, and Storm Runner moved from fifth to third for Conflicting Preferences.
Lofi and Rock kept the same order, with some score changes. The baseline weights
are restored. Without listener feedback, these results do not measure accuracy.
See the [saved outputs and comparisons](model_card.md#7-evaluation).

---

## Limitations and Risks

The 18-song catalog has only one rock song, compared with three lofi songs.
Listeners asking for rock have fewer exact matches. The experimental conflicting
profile had no sad songs in its top three because its sad options have low
energy. Repeatedly favoring similar music could create a filter bubble, but
these runs do not test long-term effects. See the [limitations](model_card.md#6-limitations-and-bias).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



