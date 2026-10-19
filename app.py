import json
import random

import streamlit as st


# ---------------------------------------------------------------- word lists
# Dolch sight word lists (public domain). Edit freely to match your school's list.
LEVELS = {
    3: {
        "name": "Pre-Primer",
        "emoji": "🐣",
        "words": [
            "a", "and", "away", "big", "blue", "can", "come", "down", "find",
            "for", "funny", "go", "help", "here", "I", "in", "is", "it",
            "jump", "little", "look", "make", "me", "my", "not", "one",
            "play", "red", "run", "said", "see", "the", "three", "to", "two",
            "up", "we", "where", "yellow", "you",
        ],
    },
    4: {
        "name": "Primer",
        "emoji": "🐥",
        "words": [
            "all", "am", "are", "at", "ate", "be", "black", "brown", "but",
            "came", "did", "do", "eat", "four", "get", "good", "have", "he",
            "into", "like", "must", "new", "no", "now", "on", "our", "out",
            "please", "pretty", "ran", "ride", "saw", "say", "she", "so",
            "soon", "that", "there", "they", "this", "too", "under", "want",
            "was", "well", "went", "what", "white", "who", "will", "with",
            "yes",
        ],
    },
    5: {
        "name": "First Grade",
        "emoji": "🦊",
        "words": [
            "after", "again", "an", "any", "as", "ask", "by", "could",
            "every", "fly", "from", "give", "giving", "had", "has", "her",
            "him", "his", "how", "just", "know", "let", "live", "may", "of",
            "old", "once", "open", "over", "put", "round", "some", "stop",
            "take", "thank", "them", "then", "think", "walk", "were", "when",
        ],
    },
    6: {
        "name": "Second Grade",
        "emoji": "🦁",
        "words": [
            "always", "around", "because", "been", "before", "best", "both",
            "buy", "call", "cold", "does", "don't", "fast", "first", "five",
            "found", "gave", "goes", "green", "its", "made", "many", "off",
            "or", "pull", "read", "right", "sing", "sit", "sleep", "tell",
            "their", "these", "those", "upon", "us", "use", "very", "wash",
            "which", "why", "wish", "work", "would", "write", "your",
        ],
    },
}

st.set_page_config(page_title="Word Explorers", page_icon="🌈", layout="centered")

PRAISE = ["Great job!", "Super reading!", "You got it!", "Amazing!", "Well done!", "Fantastic!", "Brilliant!"]
TRY_AGAIN = ["Oops! Try again!", "Almost! Have another go!", "Not quite. You can do it!"]

# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&display=swap');
html, body, [class*="css"], .stApp, button, p, h1, h2, h3, label, div {
  font-family: 'Baloo 2', 'Comic Sans MS', cursive !important;
}
.stApp {
  background: linear-gradient(135deg, #fff6d6 0%, #ffe0f0 35%, #dff3ff 70%, #e6ffe6 100%);
}
#MainMenu, footer, header {visibility: hidden;}
.title {
  text-align: center; font-size: 3.2rem !important; font-weight: 800; margin: 0; line-height:1.2;
  background: linear-gradient(90deg,#FF6B6B,#FFB830,#6BCB77,#4D96FF,#B26BFF);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.emo {color: initial; -webkit-text-fill-color: initial;}
.subtitle {text-align:center; font-size:1.4rem !important; color:#7a5c9e; margin-top:-8px;}
.prompt {text-align:center; font-size:2.1rem !important; font-weight:800; color:#4b3b8f; margin: 6px 0;}
.stars {text-align:center; font-size:1.8rem !important; min-height:1em;}
.wordcard {
  text-align:center; font-size:6rem; font-weight:800; color:#fff;
  background: linear-gradient(135deg,#B26BFF,#4D96FF);
  border-radius: 36px; padding: 10px 0 18px; margin: 10px 0 18px;
  box-shadow: 0 10px 0 #6b4bbd;
}
.bubble {
  text-align:center; font-size:2rem; font-weight:800; border-radius:28px;
  padding: 10px; margin: 12px 0; animation: pop .35s ease-out;
}
.good {background:#d9ffd6; color:#1f8a2e; border:4px solid #6BCB77;}
.bad  {background:#ffe1e1; color:#c0392b; border:4px solid #FF6B6B; animation: shake .45s;}
@keyframes pop {0%{transform:scale(.6)} 80%{transform:scale(1.08)} 100%{transform:scale(1)}}
@keyframes shake {0%,100%{transform:translateX(0)} 20%,60%{transform:translateX(-12px)} 40%,80%{transform:translateX(12px)}}
.grownup {text-align:center; color:#7a5c9e; font-size:1.2rem !important; margin-top:14px;}
.chip {display:inline-block; background:#fff; border:3px solid #FFB830; border-radius:18px;
  padding:2px 14px; margin:4px; font-size:1.6rem; font-weight:700; color:#4b3b8f;}

.stRadio p, .stCheckbox p {font-size:1.25rem !important;}

/* every button: big, round, chunky */
.stButton > button {
  width: 100%; border-radius: 28px; border: none; font-weight: 800;
  color: white; box-shadow: 0 6px 0 rgba(0,0,0,.18); transition: transform .08s;
}
.stButton > button:active {transform: translateY(4px); box-shadow: 0 2px 0 rgba(0,0,0,.18);}
.stButton > button p {font-size: 1.5rem;}
.stButton > button:disabled {opacity: .35;}

/* answer cards */
[class*="st-key-opt_"] button {min-height: 130px;}
[class*="st-key-opt_"] button p {font-size: 3.6rem !important; line-height: 1;}
.st-key-opt_0 button {background:#FF6B6B;}
.st-key-opt_1 button {background:#4D96FF;}
.st-key-opt_2 button {background:#6BCB77;}
.st-key-opt_3 button {background:#FFB830;}

.st-key-next button, .st-key-start button, .st-key-again button {
  background: linear-gradient(90deg,#B26BFF,#FF6B9E); min-height: 80px;}
.st-key-read_ok button {background:#6BCB77; min-height: 80px;}
.st-key-read_retry button {background:#FFB830; min-height: 80px;}
.st-key-home button, .st-key-quit button {background:#9aa5b1;}
.stProgress > div > div > div > div {background: linear-gradient(90deg,#FF6B6B,#FFB830,#6BCB77,#4D96FF);}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- speech
def speak(auto_text, button_text, nonce, autoplay=True, label="🔊 Hear the word"):
    """Browser text-to-speech. The button is inside the iframe so taps always work."""
    html = (
        f"""
<!-- {nonce} -->
<div style="text-align:center">
<button id="b" style="font-family:'Comic Sans MS',cursive;font-size:22px;font-weight:700;
  background:#B26BFF;color:#fff;border:none;border-radius:24px;padding:10px 28px;
  box-shadow:0 5px 0 #7d45c4;cursor:pointer">{label}</button></div>
<script>
function say(t){{
  const s = window.speechSynthesis; if(!s) return;
  s.cancel();
  const u = new SpeechSynthesisUtterance(t);
  u.rate = 0.8; u.pitch = 1.15;
  const v = s.getVoices().find(v => /en[-_](GB|SG|AU|US)/i.test(v.lang));
  if (v) u.voice = v; u.lang = v ? v.lang : 'en-GB';
  s.speak(u);
}}
document.getElementById('b').onclick = () => say({json.dumps(button_text)});
{"setTimeout(() => say(" + json.dumps(auto_text) + "), 350);" if autoplay and auto_text else ""}
</script>"""
    )
    if hasattr(st, "iframe"):
        st.iframe(html, height=70)
    else:  # older Streamlit
        import streamlit.components.v1 as components
        components.html(html, height=70)


# ---------------------------------------------------------------- state
ss = st.session_state
ss.setdefault("phase", "setup")
ss.setdefault("nonce", 0)
ss.setdefault("celebrate", False)


def word_pool():
    if ss.cumulative:
        return [w for a in LEVELS if a <= ss.age for w in LEVELS[a]["words"]]
    return list(LEVELS[ss.age]["words"])


def start_quiz():
    words = word_pool()
    random.shuffle(words)
    if ss.count != "All":
        words = words[: int(ss.count)]
    ss.queue, ss.idx = words, 0
    ss.missed, ss.requeued = [], set()
    ss.first_try = 0
    ss.phase = "quiz"
    new_question()


def begin():
    ss.age, ss.mode, ss.count, ss.cumulative = ss.w_age, ss.w_mode, ss.w_count, ss.w_cumul
    start_quiz()


def new_question():
    word = ss.queue[ss.idx]
    n_opts = 3 if ss.age == 3 else 4
    pool = [w for w in word_pool() if w != word]
    opts = random.sample(pool, n_opts - 1) + [word]
    random.shuffle(opts)
    ss.options, ss.wrong, ss.tries = opts, [], 0
    ss.status = "asking"
    ss.praise = random.choice(PRAISE)
    ss.nonce += 1


def got_it_right():
    ss.tries += 1
    if ss.tries == 1:
        ss.first_try += 1
    ss.status = "correct"
    ss.praise = random.choice(PRAISE)
    ss.celebrate = True
    ss.nonce += 1


def got_it_wrong(choice=None):
    word = ss.queue[ss.idx]
    ss.tries += 1
    ss.status = "wrong"
    ss.oops = random.choice(TRY_AGAIN)
    if choice is not None:
        ss.wrong.append(choice)
    if word not in ss.missed:
        ss.missed.append(word)
    if word not in ss.requeued:  # ask it once more at the end for extra practice
        ss.queue.append(word)
        ss.requeued.add(word)
    ss.nonce += 1


def choose(opt):
    if ss.status == "correct":
        return
    if opt == ss.queue[ss.idx]:
        got_it_right()
    else:
        got_it_wrong(opt)


def next_question():
    ss.idx += 1
    if ss.idx >= len(ss.queue):
        ss.phase = "done"
        ss.celebrate = True
    else:
        new_question()


def go_home():
    ss.phase = "setup"


# ---------------------------------------------------------------- screens
def setup_screen():
    st.markdown('<p class="title"><span class="emo">🌈</span> Word Explorers</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Let\'s read our special words!</p>', unsafe_allow_html=True)

    st.radio(
        "How old is our reader?",
        options=list(LEVELS),
        format_func=lambda a: f"{LEVELS[a]['emoji']} {a} years · {LEVELS[a]['name']} ({len(LEVELS[a]['words'])} words)",
        key="w_age",
    )
    st.radio(
        "Game",
        options=["listen", "read"],
        format_func=lambda m: {
            "listen": "👂 Listen & Find: hear the word, tap it",
            "read": "🗣️ Read Aloud: child reads, grown-up checks",
        }[m],
        key="w_mode",
    )
    st.radio("How many words?", options=["All", "10", "20"], horizontal=True, key="w_count",
             format_func=lambda c: "The full list" if c == "All" else f"{c} words")
    st.checkbox("Also include words from younger ages", key="w_cumul")
    st.button("🚀 Let's go!", key="start", on_click=begin, width="stretch")


def quiz_screen():
    word = ss.queue[ss.idx]
    total = len(ss.queue)
    lvl = LEVELS[ss.age]

    st.markdown(f'<p class="subtitle">{lvl["emoji"]} {lvl["name"]} · word {ss.idx + 1} of {total}</p>',
                unsafe_allow_html=True)
    st.progress(ss.idx / total)
    st.markdown(f'<div class="stars">{"⭐" * min(ss.first_try, 20)}{" +" + str(ss.first_try - 20) if ss.first_try > 20 else ""}</div>',
                unsafe_allow_html=True)

    if ss.mode == "listen":
        listen_round(word)
    else:
        read_round(word)

    st.write("")
    st.button("🏠 Stop and go home", key="quit", on_click=go_home, width="stretch")


def feedback(word):
    if ss.status == "correct":
        st.markdown(f'<div class="bubble good">🎉 {ss.praise} That says “{word}”!</div>', unsafe_allow_html=True)
        st.button("Next word ➡️", key="next", on_click=next_question, width="stretch")
    elif ss.status == "wrong":
        st.markdown(f'<div class="bubble bad">🙈 {ss.oops}</div>', unsafe_allow_html=True)


def listen_round(word):
    st.markdown('<p class="prompt">👂 Listen, then tap the word!</p>', unsafe_allow_html=True)
    if ss.status == "correct":
        speak(f"{ss.praise} That says {word}.", word, ss.nonce)
    elif ss.status == "wrong":
        speak(f"Try again. Find the word: {word}", word, ss.nonce)
    else:
        speak(f"Find the word: {word}", word, ss.nonce)

    for row in range(0, len(ss.options), 2):
        cols = st.columns(2)
        for j, opt in enumerate(ss.options[row:row + 2]):
            i = row + j
            label = opt
            if opt in ss.wrong:
                label = f"❌ {opt}"
            elif ss.status == "correct" and opt == word:
                label = f"✅ {opt}"
            with cols[j]:
                st.button(label, key=f"opt_{i}", on_click=choose, args=(opt,), width="stretch",
                          disabled=(opt in ss.wrong) or (ss.status == "correct" and opt != word))
    feedback(word)


def read_round(word):
    st.markdown('<p class="prompt">🗣️ Can you read this word?</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="wordcard">{word}</div>', unsafe_allow_html=True)

    if ss.status == "correct":
        speak(f"{ss.praise} {word}!", word, ss.nonce)
        feedback(word)
        return
    if ss.status == "wrong":
        st.markdown(f'<div class="bubble bad">🙈 {ss.oops}</div>', unsafe_allow_html=True)
        speak(f"Listen. This word is {word}. Now you say it!", word, ss.nonce, label="🔊 Hear it again")
    else:
        speak("", word, ss.nonce, autoplay=False, label="🔊 Need help? Hear it")

    st.markdown('<p class="grownup">👩‍🏫 For grown-ups: did they read it correctly?</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button("✅ Yes!", key="read_ok", on_click=got_it_right, width="stretch")
    c2.button("🔁 Try again", key="read_retry", on_click=got_it_wrong, width="stretch")


def done_screen():
    total = len(ss.queue)
    st.markdown('<p class="title"><span class="emo">🏆</span> You did it!</p>', unsafe_allow_html=True)
    speak("Hooray! You finished all your words!", "Hooray! You finished all your words!", ss.nonce,
          label="🔊 Hooray!")
    st.markdown(f'<div class="stars">{"⭐" * min(ss.first_try, 40)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bubble good">{ss.first_try} of {total} right on the first try!</div>',
                unsafe_allow_html=True)
    if ss.missed:
        st.markdown('<p class="prompt">📚 Words to practise</p>', unsafe_allow_html=True)
        st.markdown("".join(f'<span class="chip">{w}</span>' for w in ss.missed), unsafe_allow_html=True)
    else:
        st.markdown('<p class="prompt">🌟 Perfect! Every word right first time!</p>', unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns(2)
    c1.button("🔄 Play again", key="again", on_click=start_quiz, width="stretch")
    c2.button("🏠 Home", key="home", on_click=go_home, width="stretch")


# ---------------------------------------------------------------- main
if ss.celebrate:
    st.balloons()
    ss.celebrate = False

if ss.phase == "setup":
    setup_screen()
elif ss.phase == "quiz":
    quiz_screen()
else:
    done_screen()
