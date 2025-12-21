import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse

# --- Spotify Setup ---
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="e3b46f0da40e42e9a9a04f2fee57bb77",
    client_secret="2fa16506ca6f442cbe40753e38e46a6c"
))
st.set_page_config("🎧 Vidya's Music Recommended System", layout="centered")

# --- CSS Backgrounds ---
WELCOME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap');
html, body, [class*="css"] {
  font-family: 'Orbitron', sans-serif;
  font-size: 22px;
  color: white;
  background:
    linear-gradient(120deg, rgba(28,28,60,0.8), rgba(63,63,145,0.8)),
    url('https://source.unsplash.com/1600x900/?music-notes') center/cover no-repeat;
  background-size: 500% 500%;
  animation: welcomeFlow 30s ease infinite;
}
@keyframes welcomeFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
div.stButton > button {
  background-color: #1DB954;
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 12px;
  padding: 12px 20px;
  box-shadow: 0 0 15px #1DB954;
}
</style>
"""

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap');
html, body, [class*="css"] {
  font-family: 'Orbitron', sans-serif;
  font-size: 22px;
  color: white;
  background:
    linear-gradient(-45deg, rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
    url('https://source.unsplash.com/1600x900/?sound-wave') center/cover no-repeat;
  background-size: 600% 600%;
  animation: mainGlow 20s ease infinite;
}
@keyframes mainGlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
div.stButton > button {
  background-color: #1DB954;
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 12px;
  padding: 12px 20px;
  box-shadow: 0 0 15px #1DB954;
}
</style>
"""

RECOMMENDED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap');
html, body, [class*="css"] {
  font-family: 'Orbitron', sans-serif;
  font-size: 22px;
  color: white;
  background:
    linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
    url('https://source.unsplash.com/1600x900/?equalizer') center/cover no-repeat;
  background-size: cover;
}
div.stButton > button {
  background-color: #1DB954;
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 12px;
  padding: 12px 20px;
  box-shadow: 0 0 15px #1DB954;
}
</style>
"""

# --- Stage Styling Logic ---
if "username" not in st.session_state or not st.session_state.username:
    st.markdown(WELCOME_CSS, unsafe_allow_html=True)
else:
    st.markdown(MAIN_CSS, unsafe_allow_html=True)

# --- Welcome / Name Entry ---
if "username" not in st.session_state:
    st.session_state.username = ""
if not st.session_state.username:
    st.markdown("""
    <div style='text-align:center; padding-top:20vh;'>
      <h1 style='font-size:2.8em;
                 background:-webkit-linear-gradient(#00ffee,#1DB954);
                 -webkit-background-clip:text;
                 -webkit-text-fill-color:transparent;'>
        🎵 Vidya’s Music Recommended System
      </h1>
      <p style='color:white;'>Who is using the app now?</p>
    </div>
    """, unsafe_allow_html=True)
    name = st.text_input("Your name")
    if name:
        st.session_state.username = name.strip().capitalize()
        st.rerun()
    st.stop()

# --- Greet User ---
st.markdown(f"### 👋 Hey, **{st.session_state.username}**, this is for you 🎧")

# --- App Data ---
MOODS = ["Happy", "Romantic", "Sad", "Angry", "Fearful", "Surprised/Chill"]
LANGUAGES = ["English", "Hindi", "Tamil", "Telugu"]
EMOJIS = {
    "Happy":"🎺","Romantic":"🎻","Sad":"🎼",
    "Angry":"🥁","Fearful":"🎷","Surprised/Chill":"🎹"
}
PLAYLIST_MAP = {
    "English":{"Happy":"Happy Hits","Romantic":"All Out 00s Love","Sad":"Life Sucks",
               "Angry":"Rock Hard","Fearful":"Dark & Stormy","Surprised/Chill":"Chill Tracks"},
    "Hindi":{"Happy":"Bollywood Dance Music","Romantic":"Bollywood Romance","Sad":"Hindi Sad Songs",
             "Angry":"Desi Party Mix","Fearful":"Soulful Hindi","Surprised/Chill":"Hindi Indie Mix"},
    "Tamil":{"Happy":"Tamil Party","Romantic":"Tamil Love Songs","Sad":"Sad Tamil Songs",
             "Angry":"Tamil Mass Bangers","Fearful":"Soulful Tamil","Surprised/Chill":"Tamil Chill"},
    "Telugu":{"Happy":"Telugu Hot Hits","Romantic":"Telugu Love Songs","Sad":"Sad Telugu Songs",
              "Angry":"Telugu Party Bangers","Fearful":"Telugu Soulful","Surprised/Chill":"Chill Telugu"}
}
LATEST_2025 = {
    "English":"https://music.youtube.com/playlist?list=PLQEvGXG7yMBlKjZZaO0EXBXT5N0xVcXMe",
    "Hindi":"https://music.youtube.com/playlist?list=PLFFyMei_d85XB2mHMxHSC2RDOhyOlsvXq",
    "Tamil":"https://www.youtube.com/playlist?list=PL3oW2tjiIxvTaC6caIGR55W3ssqGvb_LR",
    "Telugu":"https://www.youtube.com/playlist?list=PLNCA1T91UH32ht6Zar4pMrEalhWp4dbAM"
}

# --- User Inputs ---
mood = st.selectbox("🎭 Select Mood", MOODS)
lang = st.selectbox("🌐 Select Language", LANGUAGES)
experience = st.radio("🎚️ Experience", ["Spotify", "YouTube"])
show_lyrics = st.checkbox("🎤 Show YouTube Lyrics")

# --- Helper: Fetch Tracks ---
def fetch_tracks(playlist_name: str, mood: str, lang: str, limit: int = 10):
    results = []
    try:
        # 1) Try playlist search
        q_pl = playlist_name
        res_pl = sp.search(q=q_pl, type="playlist", limit=1, market="IN")
        items_pl = res_pl.get("playlists", {}).get("items", [])
        if items_pl:
            pid = items_pl[0]["id"]
            items = sp.playlist_items(pid, limit=limit).get("items", [])
            results = [
                {"title":t["track"]["name"], "artist":t["track"]["artists"][0]["name"],
                 "url":t["track"]["external_urls"]["spotify"]}
                for t in items if t.get("track")
            ]
        # 2) Fallback to track search by mood+language
        if not results:
            q_tr = f"{lang} {mood} songs"
            res_tr = sp.search(q=q_tr, type="track", limit=limit, market="IN")
            items_tr = res_tr.get("tracks", {}).get("items", [])
            results = [
                {"title":t["name"], "artist":t["artists"][0]["name"],
                 "url":t["external_urls"]["spotify"]}
                for t in items_tr
            ]
    except:
        results = []
    return results

def yt_lyrics_url(title: str, artist: str) -> str:
    q = f"{title} {artist} lyrics"
    return "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q)

# --- Recommendation Action ---
if st.button("🚀 Recommend"):
    # switch to recommended background
    st.markdown(RECOMMENDED_CSS, unsafe_allow_html=True)

    emoji = EMOJIS.get(mood, "🎵")
    playlist_name = PLAYLIST_MAP.get(lang, {}).get(mood, f"{lang} {mood} Mix")
    st.subheader(f"{emoji} {mood} — {lang}")
    st.markdown("---")

    tracks = fetch_tracks(playlist_name, mood, lang)
    if experience == "Spotify":
        st.markdown(f"▶️ Playlist: [{playlist_name}](https://open.spotify.com/search/{urllib.parse.quote_plus(playlist_name)})")
        if tracks:
            for t in tracks:
                st.markdown(f"🎵 **{t['title']}** — *{t['artist']}*")
                st.markdown(f"[▶️ Listen on Spotify]({t['url']})")
                if show_lyrics:
                    st.markdown(f"[🎤 Lyrics]({yt_lyrics_url(t['title'], t['artist'])})")
                st.markdown("---")
        else:
            st.warning("⚠️ No tracks found. Try another mood or language.")
    else:
        q = urllib.parse.quote_plus(f"{lang} {mood} songs")
        st.video(f"https://www.youtube.com/embed?listType=search&list={q}")
        st.markdown(f"🔗 [Explore more on YouTube](https://www.youtube.com/results?search_query={q})")

    if lang in LATEST_2025:
        st.markdown("## 🆕 Latest Songs of 2025")
        st.markdown(f"[▶️ Listen to 2025 {lang} Playlist]({LATEST_2025[lang]})")