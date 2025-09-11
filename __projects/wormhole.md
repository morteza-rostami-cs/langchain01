https://chatgpt.com/c/68c11ef8-be98-8328-b107-7926f505aeff

OHHH I love this direction 🚀🌌 — a text-based **infinite wormhole roguelike** where each “hop” is a random story beat controlled by the LLM. Let’s polish and solidify it into something you can actually start building:

---

# 🌌 **Wormhole Odyssey (working title)**

### 🎯 **Core Gameplay Loop**

1. Player starts with some **basic stats**:

   - Health 💖
   - Sanity 🧠
   - Inventory 🎒 (empty at first)

2. Each turn:

   - Player walks into a **wormhole** → arrives on a random planet.
   - Encounters an **NPC** (role-played by the LLM). NPC has a _type_:

     - **Friendly** → offers loot, tips, or healing.
     - **Neutral Trickster** → gives riddles/puzzles. Correct → loot. Wrong → hostile.
     - **Hostile** → attacks or traps player immediately.
     - **Chaotic/Unhinged** → nonsense, unpredictable (maybe lies, maybe helps, maybe eats your shoe).

3. After resolving encounter:

   - Three **new wormholes** appear.
   - Player chooses one → cycle repeats.

4. Game ends when:

   - Health or Sanity hits **0**.
   - (Optional) Player chooses to “retire” and log their adventure.

---

### 🧩 **Mechanics**

- **Stats System**

  - Health: lost in fights / gained via healing items.
  - Sanity: lost from weird encounters / regained via nice NPCs.
  - Inventory: holds loot, keys, weapons.

- **Combat**

  - Super light (just “fight/defend/run”).
  - Outcomes narrated by LLM + some RNG.

- **Loot**

  - Potions, artifacts, cursed items (affect sanity).
  - Maybe “wormhole tokens” to influence choice.

- **Choice Weighting**

  - Each wormhole could be labeled _mysterious, glowing, unstable_.
  - LLM uses descriptors to hint at outcomes but keeps it vague.

---

### 🖥️ **Architecture**

- **Frontend (Vue.js)**

  - Text adventure console (like old terminal).
  - Player input box for choices.
  - Inventory + stats bar at the side.
  - Wormhole choice cards after each encounter.

- **Backend (FastAPI)**

  - `POST /start` → create new game session.
  - `POST /event` → resolve encounter (calls LLM with LangChain).
  - `POST /choose-wormhole` → advances story.
  - `GET /state` → return current stats/inventory.

- **LLM Orchestration (LangChain + Ollama)**

  - Prompt templates for each NPC type.
  - Memory chain to track:

    - Player stats & items.
    - Past encounters (NPCs may reference them later).

---

### 🎨 **Example Flow**

1. **Intro:**
   “You step into the machine. Reality tears. You emerge in a world of green oceans and floating castles.”

2. **NPC:**

   - Type: Trickster.
   - LLM says: _“Answer my riddle, traveler: I speak without a mouth and hear without ears…”_
   - Player: “Echo.”
   - Outcome: Trickster cackles, tosses you a glowing gem → +10 sanity.

3. **Next Choice:**
   “Before you shimmer three wormholes:”

   - Left: _unstable, crackling red energy_
   - Middle: _calm, steady pulse of blue_
   - Right: _whispers of laughter echo from within_

4. **Loop continues…**

---

### 🔥 **Fun Add-ons (optional later)**

- **Leaderboards** (longest survival).
- **Lore generator** → random planets get backstory.
- **Evil NPC memory** → one might _follow you_ through wormholes.
- **Player “last words” log** when they die (saved in DB).

---

This design gives you:
✅ Infinite replayability.
✅ Heavy LLM roleplay.
✅ Mix of **structured mechanics + chaotic unpredictability** (perfect balance for fun).
✅ Expandable over time.

---

👉 Do you want me to **sketch out the actual LangChain flow & prompt templates** for generating NPC encounters (friendly, hostile, riddler, chaotic), so you can plug them into FastAPI right away?

## if retired => sent to a random planet, one choice! could be bad or good!
