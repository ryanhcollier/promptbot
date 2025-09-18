# ---------- Streamlit Video Prompt Generator ----------

import streamlit as st
import json

# --- Page Config ---
st.set_page_config(
    page_title="AI Prompt Generator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Define Presets and Options ---
DIRECTOR_OPTIONS = [
    "Steven Spielberg & Bill Butler (Jaws)",
    "Steven Spielberg & Janusz Kamiński (Saving Private Ryan)",
    "Christopher Nolan & Wally Pfister (The Dark Knight Trilogy, Inception)",
    "Christopher Nolan & Hoyte van Hoytema (Interstellar, Dunkirk, Tenet, Oppenheimer)",
    "Martin Scorsese & Michael Ballhaus (Goodfellas)",
    "Quentin Tarantino & Robert Richardson (Kill Bill Vol. 1 & 2, Once Upon a Time in Hollywood)",
    "Paul Thomas Anderson & Robert Elswit (There Will Be Blood, Inherent Vice)",
    "Wes Anderson & Robert Yeoman (The Royal Tenenbaums, Moonrise Kingdom, The Grand Budapest Hotel)",
    "David Fincher & Jeff Cronenweth (Fight Club, The Social Network, The Girl with the Dragon Tattoo)",
    "Denis Villeneuve & Roger Deakins (Prisoners, Sicario, Blade Runner 2049)",
    "Denis Villeneuve & Greig Fraser (Dune: Part One & Two)",
    "Alejandro González Iñárritu & Emmanuel “Chivo” Lubezki (Birdman, The Revenant)",
    "Terrence Malick & Néstor Almendros (Days of Heaven)",
    "Darren Aronofsky & Matthew Libatique (Pi, Requiem for a Dream, The Fountain, Black Swan, Mother!)"
]

# --- Functions ---

def generate_prompt_from_state():
    """Generates prompt from session state variables."""
    answers = {key: st.session_state.get(key, "") for key in st.session_state.keys()}

    prompt_lines = []
    # Using a fixed order for the prompt to match original output
    ordered_keys = [
        "realism", "emotional_theme", "director_shot_by", "scene_details", "camera_angle",
        "environment", "imperfections", "time_of_day", "season", "lighting",
        "scene_materials", "atmosphere", "color_palette", "character_details",
        "gender", "ethnicity", "age", "pose_body", "body_type", "hands_gestures",
        "eyes", "skin", "mouth", "hair", "clothing", "background_depth",
        "reflections", "subsurface", "caustics", "lens", "camera_model",
        "shutter_speed", "focus_depth", "camera_movement", "film_processing",
        "film_stock", "framing", "mood", "cultural", "aspect_ratio",
        "resolution", "grain", "additional_notes"
    ]

    for key in ordered_keys:
        if key in answers and answers[key]:
            formatted_key = key.replace('_', ' ').title()
            prompt_lines.append(f"- {formatted_key}: {answers[key]}")

    if prompt_lines:
        return "Merge the following answers into a single descriptive paragraph...\n\n" + "\n".join(prompt_lines)
    else:
        return ""

def clear_all_fields():
    """Clears all input fields by setting their session state values to empty strings."""
    for key in st.session_state.keys():
        st.session_state[key] = ""
    # Update the prompt output to be empty
    st.session_state.generated_prompt = ""
    st.experimental_rerun()

def save_preset():
    """Saves the current inputs to a JSON string."""
    preset_data = {key: st.session_state.get(key, "") for key in st.session_state.keys()}
    return json.dumps(preset_data, indent=4)

def load_preset(uploaded_file):
    """Loads a preset from an uploaded JSON file."""
    if uploaded_file is not None:
        try:
            preset_data = json.load(uploaded_file)
            for key, value in preset_data.items():
                if key in st.session_state:
                    st.session_state[key] = value
            st.success("Preset loaded successfully!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Failed to load preset file: {e}")

# --- UI Layout ---

st.title("AI Prompt Generator")

tab1, tab2, tab3, tab4 = st.tabs(["Scene & Style", "Subject & Character", "Camera & Lens", "Post-Processing"])

# Use a dictionary to hold all input widgets
input_widgets = {}

with tab1:
    input_widgets["realism"] = st.text_area("Realism level (Photo Realistic, painterly, cartoon, stylized)", key="realism", height=100)
    input_widgets["emotional_theme"] = st.text_area("Describe the emotional theme (joy, fear, love, tension)", key="emotional_theme", height=100)
    input_widgets["mood"] = st.text_area("Mood & style (dark, playful, suspenseful, whimsical)", key="mood", height=100)
    input_widgets["cultural"] = st.text_area("Cultural influence (cyberpunk Tokyo, Afrofuturism, Mayan temples)", key="cultural", height=100)
    input_widgets["scene_details"] = st.text_area("Describe the scene (location, environment, landscape, single or group of people)", key="scene_details", height=100)
    input_widgets["environment"] = st.text_area("Describe the environment and setting (architecture, materials, vibe)", key="environment", height=100)
    input_widgets["imperfections"] = st.text_area("Describe the environment imperfections (scratches, dust, chipped paint)", key="imperfections", height=100)
    input_widgets["time_of_day"] = st.text_area("Time of day (dawn, golden hour, twilight, midnight)", key="time_of_day", height=100)
    input_widgets["season"] = st.text_area("Season or climate (spring bloom, autumn leaves, summer heat, winter cold)", key="season", height=100)
    input_widgets["lighting"] = st.text_area("Describe lighting & weather (soft, harsh, natural, artificial)", key="lighting", height=100)
    input_widgets["scene_materials"] = st.text_area("Describe materials & textures in the scene (stained concrete, velvet, rough leather)", key="scene_materials", height=100)
    input_widgets["atmosphere"] = st.text_area("Describe the atmosphere (haze, fog, smoke, underwater, dust)", key="atmosphere", height=100)
    input_widgets["color_palette"] = st.text_area("Color palette (60/30/10 rule, color harmony, tone)", key="color_palette", height=100)

with tab2:
    input_widgets["character_details"] = st.text_area("Describe the characters (emotions, props, context)", key="character_details", height=100)
    input_widgets["gender"] = st.text_area("Gender (male, female, androgynous)", key="gender", height=100)
    input_widgets["ethnicity"] = st.text_area("Ethnicity (Chinese, Indian, Nigerian, Italian, etc.)", key="ethnicity", height=100)
    input_widgets["age"] = st.text_area("Age Specificity (toddler, teenager, mid-30s, elderly)", key="age", height=100)
    input_widgets["pose_body"] = st.text_area("Pose & Body Language (standing tall, slouched, walking, fighting, dancing)", key="pose_body", height=100)
    input_widgets["body_type"] = st.text_area("Body Type (slim, obese, muscular, athletic)", key="body_type", height=100)
    input_widgets["hands_gestures"] = st.text_area("Hands & Gestures (open palms, gripping object, hidden, expressive)", key="hands_gestures", height=100)
    input_widgets["eyes"] = st.text_area("Describe the eyes (color, expression, gaze direction)", key="eyes", height=100)
    input_widgets["skin"] = st.text_area("Describe the skin in detail(tone, texture, imperfections, makeup (very important step))", key="skin", height=100)
    input_widgets["mouth"] = st.text_area("Describe the mouth (shape, fullness, emotion)", key="mouth", height=100)
    input_widgets["hair"] = st.text_area("Describe the hair (color, thickness, style, length)", key="hair", height=100)
    input_widgets["clothing"] = st.text_area("Describe the clothing (style, color palette, texture, brand, imperfections)", key="clothing", height=100)

with tab3:
    input_widgets["director_shot_by"] = st.selectbox("Director / Cinematographer Pair", options=DIRECTOR_OPTIONS, key="director_shot_by")
    input_widgets["camera_angle"] = st.text_area("Describe camera angle and framing (worm’s-eye, wide shot, close-up)", key="camera_angle", height=100)
    input_widgets["framing"] = st.text_area("Framing style (center frame, leading lines, frame-in-frame)", key="framing", height=100)
    input_widgets["lens"] = st.text_area("Lens details (12mm wide, 50mm natural, f-stop for bokeh)", key="lens", height=100)
    input_widgets["camera_model"] = st.text_area("Camera model/sensor type (ARRI Alexa, RED Komodo, Leica M10)", key="camera_model", height=100)
    input_widgets["focus_depth"] = st.text_area("Focus depth (macro detail, shallow focus, deep focus)", key="focus_depth", height=100)
    input_widgets["shutter_speed"] = st.text_area("Shutter speed / motion (motion blur, frozen action, long exposure)", key="shutter_speed", height=100)
    input_widgets["camera_movement"] = st.text_area("Describe the overall camera movement (Pan, Tilt, Dolly)", key="camera_movement", height=100)
    input_widgets["background_depth"] = st.text_area("Background depth (shallow DOF, detailed, blurred)", key="background_depth", height=100)
    input_widgets["reflections"] = st.text_area("Describe reflections & refractions (wet streets, mirrors, glass flares)", key="reflections", height=100)
    input_widgets["subsurface"] = st.text_area("Describe subsurface scattering (light through ears, glow under skin)", key="subsurface", height=100)
    input_widgets["caustics"] = st.text_area("Describe caustics (light bending through water, glass prisms)", key="caustics", height=100)

with tab4:
    input_widgets["aspect_ratio"] = st.text_area("Aspect ratio (16:9, 9:16, 1:1, 4:3, 2.39:1)", key="aspect_ratio", height=100)
    input_widgets["resolution"] = st.text_area("Resolution & detail level (8K cinematic, VHS grainy)", key="resolution", height=100)
    input_widgets["grain"] = st.text_area("Noise / grain (film grain, digital clean, noisy low-light)", key="grain", height=100)
    input_widgets["film_processing"] = st.text_area("Film processing look (35mm, vintage, iPhone aesthetic)", key="film_processing", height=100)
    input_widgets["film_stock"] = st.text_area("Film stock simulation (Kodak Portra 400, Fuji Velvia, Ilford HP5)", key="film_stock", height=100)
    input_widgets["additional_notes"] = st.text_area("Add any additional notes", key="additional_notes", height=100)

# --- Button Panel & Actions ---
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("✨ Generate Prompt", use_container_width=True):
        st.session_state.generated_prompt = generate_prompt_from_state()

with col2:
    if st.button("📋 Copy", use_container_width=True):
        st.session_state.copy_text = st.session_state.get("generated_prompt", "")
        st.toast('Copied to clipboard!', icon='📋')

with col3:
    st.download_button(
        label="💾 Save",
        data=save_preset(),
        file_name="prompt_preset.json",
        mime="application/json",
        use_container_width=True,
    )

with col4:
    uploaded_file = st.file_uploader("📂 Load", type="json", label_visibility="collapsed")
    if uploaded_file:
        load_preset(uploaded_file)

with col5:
    st.download_button(
        label="📄 Export",
        data=st.session_state.get("generated_prompt", ""),
        file_name="prompt.txt",
        mime="text/plain",
        use_container_width=True,
    )

with col6:
    if st.button("❌ Clear All", use_container_width=True):
        clear_all_fields()

# --- Output Section ---
st.markdown("---")
st.header("Generated Prompt:")
st.text_area("Output", value=st.session_state.get("generated_prompt", ""), height=300, disabled=True, label_visibility="collapsed")
