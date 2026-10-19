# 🌈 Word Explorers

A colourful sight-word game for ages 3 to 6, built with Streamlit.

## Word lists (in `words.py`)

| Age | List | Words |
|-----|------|-------|
| 3 | Dolch Pre-Primer | 40 |
| 4 | Dolch Primer | 52 |
| 5 | Dolch First Grade | 41 |
| 6 | Dolch Second Grade | 46 |

To use your school's own list, edit the words in `words.py`.
Tick "Also include words from younger ages" to test everything up to that age.

## Two games

- **👂 Listen & Find**: the app says a word, the child taps the matching card (3 cards for age 3, 4 cards for older children). Checked automatically.
- **🗣️ Read Aloud**: the word is shown big, the child reads it out, and a grown-up taps ✅ or 🔁.

In both games a wrong answer shows "Try again!" and the child stays on that word until they get it right. Missed words come back once more at the end, and the final screen lists words to practise.

## Run on your computer

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud (free)

1. Create a GitHub account and a new public repository.
2. Upload `app.py`, `words.py` and `requirements.txt` to it.
3. Go to https://share.streamlit.io, sign in with GitHub, click **Create app**.
4. Pick your repository, branch `main`, main file `app.py`, then **Deploy**.
5. You get a link (like `https://your-app.streamlit.app`) that works on any tablet or phone.

## Tips

- Turn the device volume up. The voice uses the browser's built-in speech, so it works best in Chrome or Safari.
- If the word isn't spoken automatically the first time (some tablets block sound until you tap), press **🔊 Hear the word**.
