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
Profile: Happy Pop {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

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

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



