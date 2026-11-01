# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeFinder 1.0

---

## 2. Intended Use  

VibeFinder ranks songs in a fixed CSV using a user's genre, mood, and energy
preferences. It's a classroom project for learning how recommendation rules
work. It isn't a production music service or a tool for predicting emotions.
It hasn't been validated for real listener satisfaction.

---

## 3. How the Model Works  

This content-based recommender compares each song with the user's preferred
genre (style), mood (feeling), and energy (intensity). An exact genre match earns
2 points and an exact mood match earns 1 point. Energy earns 1 minus the gap
from the user's target, with a minimum of 0 points. Closer energy is better,
not just higher energy. A perfect
match earns 4 points. The hand-chosen weights are genre=2, mood=1, and energy=1;
they aren't trained on user behavior.

The program scores every song and sorts by highest score without rounding.
Equal scores use the lowest numeric song ID first. The CLI shows the top five
with reasons showing genre points, mood points, and the energy gap, similarity,
and points. Requesting the top k returns up to k songs; an empty catalog or
nonpositive k returns none.

A small adapter turns the class profile's favorite genre, favorite mood, and
target energy into the same preferences used by the dictionary functions.
Both versions share the scoring and explanations. The class returns the original
Song objects. The likes_acoustic field stays available but does not affect scores.

---

## 4. Data  

The catalog has 18 fictional songs: the 10 starter songs plus eight synthetic
additions with IDs 11–18. The original rows and header were kept. The additions
include classical, hip-hop, folk, and EDM, with moods such as sad and nostalgic.

All ten columns are retained: id, title, artist, genre, mood, energy, tempo_bpm,
valence, danceability, and acousticness. IDs are integers; the five numerical
features are stored as floats. Genre and mood stay text, as do title and artist.
Only genre, mood, and energy affect scores. Energy, valence, danceability, and
acousticness range from 0 to 1; tempo is in beats per minute.

The catalog has 13 genre labels and uneven coverage. Lofi has three songs;
pop, folk, and synthwave have two each; the other nine genres have one each.
There are no lyrics, languages, or real listening histories, so the data covers
only a small part of musical taste.

---

## 5. Strengths  

The baseline puts clear feature matches first. Sunrise City leads Pop at 3.98:
it matches pop and happy, and its energy is close to 0.8. Library Rain leads
Lofi with a perfect 4.00 because all three features match. Storm Runner leads
Rock at 3.99 with matching rock and intense labels and energy 0.91, close to
0.9. The reasons show exactly where each song's points came from.

---

## 6. Limitations and Bias 

Of the 18 songs, lofi has 3, pop, folk, and synthwave have 2 each, and the other
9 genres have 1 each.
This gives rock listeners only one exact genre match, compared with three for
lofi, so the baseline Rock top five includes four songs from other genres.
The conflicting profile requests sad music, but no sad song reaches its
experimental top three.
Its only sad options have energy 0.19 and 0.38, so doubling energy points favors
other moods and limits choices for listeners asking for high-energy sad music.
A possible filter-bubble risk is repeatedly favoring similar songs, but these
fixed runs do not show whether that happens over time.

---

## 7. Evaluation  

Baseline: genre earns 2 points, mood earns 1, and energy earns up to 1.
The catalog has 18 songs. Before running, the expected leaders were Sunrise City
for Pop, Library Rain for Lofi, and Storm Runner for Rock. The conflicting
profile was expected to favor pop even when the mood did not match.

The four outputs below came from running `python -m src.main`.
All 21 tests passed with `python -m pytest`. These checks show how the rules
behave, not measured accuracy: there is no labeled listener feedback to use as
ground truth.

These saved outputs use the earlier list layout. The current CLI shows the same
baseline rankings, scores, and reasons in a table.

**Baseline: High-Energy Pop**

```text
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

```

**Baseline: Chill Lofi**

```text
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

```

**Baseline: Intense Rock**

```text
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

```

**Baseline: Conflicting Preferences**

```text
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

For the Pop profile, Sunrise City beats Gym Hero:

- Sunrise City: pop earns 2, happy earns 1, and energy 0.82 has a gap of 0.02
  from 0.8, earning 0.98. Total: 3.98.
- Gym Hero: pop earns 2, intense earns 0, and energy 0.93 has a gap of 0.13,
  earning 0.87. Total: 2.87.

Sunrise City wins because it matches the mood and has a smaller energy gap.

- **Pop–Lofi:** All five titles differ. Pop's leader is happy pop at energy
  0.82; Lofi's leader is chill lofi at 0.35, exactly its target. Lofi's first
  three songs all match its genre, while Pop has only two exact genre matches
  in the catalog.
- **Pop–Rock:** Storm Runner leads Rock at 3.99 instead of Sunrise City.
  Gym Hero appears in both: Pop gives it 2 genre points, 0 mood points, and
  0.87 energy points; Rock gives it 0 genre points, 1 mood point, and 0.97
  energy points. Its pop genre and intense mood explain the overlap.
- **Lofi–Rock:** No top-five titles overlap. Library Rain's chill mood and
  energy 0.35 fit Lofi; Storm Runner's intense mood and energy 0.91 fit Rock.
  Lofi also includes the chill ambient song Spacewalk Thoughts. Rock includes
  the energetic EDM song Prism Festival, even without a genre or mood match.

The conflicting profile asks for pop, sad, and energy 0.9, but no song combines
pop and sad. Gym Hero leads with 2 genre points, 0 mood points, and 0.97 energy
points. Sunrise City follows at 2.92. The sad songs Empty Station (blues,
energy 0.38) and Winter Window (classical, 0.19) get the mood point but miss
genre and have larger energy gaps. They rank third and fourth at 1.48 and 1.29.
Storm Runner ranks fifth at 0.99 from energy alone.

There are only two pop songs and one rock song, so top-five lists must include
other genres. Sunrise City (energy 0.82) and Sidewalk Summit (0.78) repeat across
Pop and Rock because their energies are close to both targets. Gym Hero,
Sunrise City, and Storm Runner also repeat in the conflicting list for the
reasons above. Genre and mood matches are rewarded, not required.

**Controlled weight experiment**

Baseline weights: genre=2.0, mood=1.0, energy=1.0.
Experimental weights: genre=1.0, mood=1.0, energy=2.0.
Only these weights and their point explanations changed. Songs, profiles,
energy similarity, and tie handling stayed the same.

**Experimental: High-Energy Pop**

```text
Profile: High-Energy Pop {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

Top recommendations:

1. Sunrise City - Score: 3.96
Because: genre match (+1.0); mood match (+1.0); energy gap 0.02, similarity 0.98 (+1.96)

2. Rooftop Lights - Score: 2.92
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.04, similarity 0.96 (+1.92)

3. Gym Hero - Score: 2.74
Because: genre match (+1.0); mood mismatch (+0.0); energy gap 0.13, similarity 0.87 (+1.74)

4. Sidewalk Summit - Score: 1.96
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.02, similarity 0.98 (+1.96)

5. Night Drive Loop - Score: 1.90
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.05, similarity 0.95 (+1.90)

```

**Experimental: Chill Lofi**

```text
Profile: Chill Lofi {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}

Top recommendations:

1. Library Rain - Score: 4.00
Because: genre match (+1.0); mood match (+1.0); energy gap 0.00, similarity 1.00 (+2.00)

2. Midnight Coding - Score: 3.86
Because: genre match (+1.0); mood match (+1.0); energy gap 0.07, similarity 0.93 (+1.86)

3. Focus Flow - Score: 2.90
Because: genre match (+1.0); mood mismatch (+0.0); energy gap 0.05, similarity 0.95 (+1.90)

4. Spacewalk Thoughts - Score: 2.86
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.07, similarity 0.93 (+1.86)

5. Coffee Shop Stories - Score: 1.96
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.02, similarity 0.98 (+1.96)

```

**Experimental: Intense Rock**

```text
Profile: Intense Rock {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}

Top recommendations:

1. Storm Runner - Score: 3.98
Because: genre match (+1.0); mood match (+1.0); energy gap 0.01, similarity 0.99 (+1.98)

2. Gym Hero - Score: 2.94
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.03, similarity 0.97 (+1.94)

3. Prism Festival - Score: 1.88
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.06, similarity 0.94 (+1.88)

4. Sunrise City - Score: 1.84
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.08, similarity 0.92 (+1.84)

5. Sidewalk Summit - Score: 1.76
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.12, similarity 0.88 (+1.76)

```

**Experimental: Conflicting Preferences**

```text
Profile: Conflicting Preferences {'genre': 'pop', 'mood': 'sad', 'energy': 0.9}

Top recommendations:

1. Gym Hero - Score: 2.94
Because: genre match (+1.0); mood mismatch (+0.0); energy gap 0.03, similarity 0.97 (+1.94)

2. Sunrise City - Score: 2.84
Because: genre match (+1.0); mood mismatch (+0.0); energy gap 0.08, similarity 0.92 (+1.84)

3. Storm Runner - Score: 1.98
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.01, similarity 0.99 (+1.98)

4. Empty Station - Score: 1.96
Because: genre mismatch (+0.0); mood match (+1.0); energy gap 0.52, similarity 0.48 (+0.96)

5. Prism Festival - Score: 1.88
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy gap 0.06, similarity 0.94 (+1.88)

```

Compared with the baseline:

- **Pop:** Rooftop Lights moves from third (1.96) to second (2.92), ahead of
  Gym Hero, which moves from second (2.87) to third (2.74). Rooftop Lights has
  happy mood and energy 0.76, closer to the 0.8 target than Gym Hero's 0.93.
  Reducing genre points and doubling energy points changes their order.
  Sunrise City stays first, changing from 3.98 to 3.96.
- **Lofi:** All five titles stay in the same order. Library Rain stays at 4.00;
  Midnight Coding changes from 3.93 to 3.86 and Spacewalk Thoughts from 1.93
  to 2.86. The perfect match keeps four points under either weight set.
- **Rock:** All five titles stay in the same order. Storm Runner changes from
  3.99 to 3.98, while Gym Hero changes from 1.97 to 2.94 because its energy
  similarity of 0.97 now earns 1.94 points instead of 0.97.
- **Conflicting Preferences:** Storm Runner moves from fifth (0.99) to third
  (1.98), based only on energy. Empty Station moves from third (1.48) to fourth
  (1.96). Prism Festival enters fifth at 1.88, and Winter Window leaves the top
  five. Gym Hero stays first, changing from 2.97 to 2.94.

All four profiles kept the same first-ranked song, but some lower ranks changed.
The experiment shows a different tradeoff, not proof that one version is more
accurate or preferred by a listener. As a feature check, the Pop leader matches
pop and happy, while the Lofi leader has much lower energy than the Rock leader.
These observations don't measure listener satisfaction.

After the experiment, the weights returned to genre=2, mood=1, and energy=1.
The final CLI rankings, scores, and reasons match all four saved baseline lists.
All 21 tests pass with these restored weights.

---

## 8. Future Work  

- Add more songs across genres, moods, and energy levels.
- Collect explicit likes and dislikes to check whether suggestions fit listeners.
- Try a diversity rule so the top five don't repeat the same artist or genre too much.

---

## 9. Personal Reflection  

The main lesson is that a recommendation depends on the data and scoring rules.
A song starts as a CSV row, gets points for matching a profile, and takes its
place in a sorted list. AI helped plan the rule, write the code and tests, and
explain the output. Checks included real CLI runs, score calculations, and
automated tests. AI's scoring explanations needed double-checking against the
CSV and the scoring rule.

A key result is that simple rules gave the three main profiles different top
songs without learning from listener behavior. The weight experiment kept the
same leaders but changed some lower ranks. That shows a different tradeoff,
not proof of better recommendations. A useful next step would be a broader
catalog and real listener feedback.
