# ---------- Video Prompt Generator ----------

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import platform
import json

# --- Core Functions ---

def get_widget_value(widget):
    """Gets the value from a widget, handling different types."""
    if isinstance(widget, scrolledtext.ScrolledText):
        return widget.get("1.0", tk.END).strip()
    elif isinstance(widget, ttk.Combobox):
        return widget.get().strip()
    return ""

def set_widget_value(widget, value):
    """Sets the value of a widget, handling different types."""
    if isinstance(widget, scrolledtext.ScrolledText):
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
    elif isinstance(widget, ttk.Combobox):
        widget.set(value)

def generate_prompt():
    """Generates the final prompt string and displays it in the output box."""
    answers = {key: get_widget_value(widget) for key, widget in boxes.items()}

    prompt_lines = []
    for key, value in answers.items():
        if value:
            # Format the key nicely for the prompt
            formatted_key = key.replace('_', ' ').title()
            prompt_lines.append(f"- {formatted_key}: {value}")

    if prompt_lines:
        final_prompt = "Merge the following answers into a single descriptive paragraph optimized for AI platforms and create a cinematic video based off the result.\n\n" + "\n".join(prompt_lines)
    else:
        final_prompt = ""

    output.delete("1.0", tk.END)
    output.insert(tk.END, final_prompt)
    return final_prompt

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output.get("1.0", tk.END).strip())
    root.update()

def clear_all_fields():
    """Clears all input fields."""
    if messagebox.askokcancel("Clear All", "Are you sure you want to clear all fields?"):
        for widget in boxes.values():
            set_widget_value(widget, "")
        output.delete("1.0", tk.END)

def save_preset():
    """Saves the current state of all input fields to a JSON file."""
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        title="Save Preset As"
    )
    if not filepath:
        return

    preset_data = {key: get_widget_value(widget) for key, widget in boxes.items()}

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(preset_data, f, indent=4)
        messagebox.showinfo("Success", "Preset saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save preset file.\nError: {e}")

def load_preset():
    """Loads a preset from a JSON file and populates the fields."""
    filepath = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        title="Load Preset"
    )
    if not filepath:
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            preset_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        messagebox.showerror("Error", f"Failed to load preset file.\nError: {e}")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred.\nError: {e}")
        return

    for key, value in preset_data.items():
        if key in boxes:
            set_widget_value(boxes[key], value)
    messagebox.showinfo("Success", "Preset loaded successfully!")

def export_to_txt():
    """Exports the generated prompt to a text file."""
    prompt_content = output.get("1.0", tk.END).strip()
    if not prompt_content:
        messagebox.showwarning("Empty Prompt", "The generated prompt is empty. Please generate a prompt first.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Export Prompt As"
    )
    if not filepath:
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        messagebox.showinfo("Success", "Prompt exported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export file.\nError: {e}")


# ---------- UI setup ----------
root = tk.Tk()
root.title("AI Prompt Generator")
root.geometry("750x750")

# --- Main Scrolling Canvas ---
canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
outer_frame = tk.Frame(canvas, padx=10, pady=10)
outer_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=outer_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

boxes = {}
labels = {}

def _on_mousewheel(event):
    if platform.system() == "Windows":
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    else: # Linux and MacOS
        # MacOS uses delta, Linux uses num
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        else: # Fallback for MacOS
             canvas.yview_scroll(int(-1 * event.delta), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# --- UI Elements ---
title_label = tk.Label(outer_frame, text="AI Prompt Generator", font=("Helvetica", 24, "bold"))
title_label.pack(pady=(0, 10))

notebook = ttk.Notebook(outer_frame)
notebook.pack(pady=10, padx=10, expand=True, fill="both")

tab_scene = ttk.Frame(notebook, padding=10)
tab_subject = ttk.Frame(notebook, padding=10)
tab_camera = ttk.Frame(notebook, padding=10)
tab_post = ttk.Frame(notebook, padding=10)

notebook.add(tab_scene, text="Scene & Style")
notebook.add(tab_subject, text="Subject & Character")
notebook.add(tab_camera, text="Camera & Lens")
notebook.add(tab_post, text="Post-Processing")

# --- Helper functions for UI elements ---
def add_input(parent, key, label_text, height=3):
    label = tk.Label(parent, text=label_text, font=("Helvetica", 12), anchor="w", justify="left")
    label.pack(pady=(5,2), anchor="w", fill="x")
    labels[key] = label

    box = scrolledtext.ScrolledText(parent, height=height, wrap=tk.WORD, font=("Helvetica", 11))
    box.pack(pady=2, anchor="w", fill="x", expand=True)
    boxes[key] = box
    return box

def add_dropdown(parent, key, label_text, options):
    label = tk.Label(parent, text=label_text, font=("Helvetica", 12), anchor="w", justify="left")
    label.pack(pady=(5,2), anchor="w", fill="x")
    labels[key] = label

    combo = ttk.Combobox(parent, values=options, font=("Helvetica", 11), state="readonly")
    combo.pack(pady=2, anchor="w", fill="x", expand=True)
    boxes[key] = combo
    return combo

# --- Dropdown Options ---
director_options = [
    "Steven Spielberg & Janusz Kamiński", "Christopher Nolan & Hoyte van Hoytema",
    "Martin Scorsese & Michael Ballhaus", "Quentin Tarantino & Robert Richardson",
    "Wes Anderson & Robert Yeoman", "David Fincher & Jeff Cronenweth",
    "Denis Villeneuve & Roger Deakins", "Denis Villeneuve & Greig Fraser",
    "Alejandro G. Iñárritu & Emmanuel Lubezki", "Terrence Malick & Néstor Almendros",
    "Darren Aronofsky & Matthew Libatique"
]

# --- Input Fields ---
# Tab 1: Scene & Style
add_dropdown(tab_scene, "realism", "Realism level", ["Photo Realistic", "Painterly", "Cartoon", "Stylized"])
add_input(tab_scene, "emotional_theme", "Emotional theme (joy, fear, love, tension)")
add_dropdown(tab_scene, "mood", "Mood & style", ["Dark", "Playful", "Suspenseful", "Whimsical", "Romantic", "Eerie"])
add_input(tab_scene, "cultural", "Cultural influence (cyberpunk Tokyo, Afrofuturism)")
add_input(tab_scene, "scene_details", "Scene description (location, environment, landscape)")
add_input(tab_scene, "environment", "Environment & setting (architecture, materials, vibe)")
add_input(tab_scene, "imperfections", "Environment imperfections (scratches, dust, chipped paint)")
add_dropdown(tab_scene, "time_of_day", "Time of day", ["Dawn", "Golden Hour", "High Noon", "Twilight", "Midnight"])
add_dropdown(tab_scene, "season", "Season or climate", ["Spring", "Summer", "Autumn", "Winter"])
add_input(tab_scene, "lighting", "Lighting & weather (soft, harsh, natural, artificial)")
add_input(tab_scene, "scene_materials", "Materials & textures in scene (concrete, velvet, leather)")
add_input(tab_scene, "atmosphere", "Atmosphere (haze, fog, smoke, underwater, dust)")
add_input(tab_scene, "color_palette", "Color palette (60/30/10 rule, color harmony, tone)")

# Tab 2: Subject & Character
add_input(tab_subject, "character_details", "Character description (emotions, props, context)")
add_dropdown(tab_subject, "gender", "Gender", ["Male", "Female", "Androgynous", "Non-binary"])
add_input(tab_subject, "ethnicity", "Ethnicity (e.g., Chinese, Indian, Nigerian, Italian)")
add_input(tab_subject, "age", "Age (e.g., toddler, teenager, mid-30s, elderly)")
add_input(tab_subject, "pose_body", "Pose & Body Language (standing tall, slouched, dancing)")
add_input(tab_subject, "body_type", "Body Type (slim, obese, muscular, athletic)")
add_input(tab_subject, "hands_gestures", "Hands & Gestures (open palms, gripping object, expressive)")
add_input(tab_subject, "eyes", "Eyes (color, expression, gaze direction)")
add_input(tab_subject, "skin", "Skin (tone, texture, imperfections, makeup)")
add_input(tab_subject, "mouth", "Mouth (shape, fullness, emotion)")
add_input(tab_subject, "hair", "Hair (color, thickness, style, length)")
add_input(tab_subject, "clothing", "Clothing (style, color, texture, brand, imperfections)")

# Tab 3: Camera & Lens
add_dropdown(tab_camera, "director_shot_by", "Director / Cinematographer Style", director_options)
add_input(tab_camera, "camera_angle", "Camera angle (worm’s-eye, wide shot, close-up)")
add_dropdown(tab_camera, "framing", "Framing style", ["Center Frame", "Leading Lines", "Rule of Thirds", "Frame-in-Frame"])
add_input(tab_camera, "lens", "Lens details (e.g., 12mm wide, 50mm, f/1.8 for bokeh)")
add_input(tab_camera, "camera_model", "Camera model/sensor (e.g., ARRI Alexa, RED Komodo, Leica M10)")
add_input(tab_camera, "focus_depth", "Focus depth (macro, shallow, deep)")
add_input(tab_camera, "shutter_speed", "Shutter speed / motion (motion blur, frozen action, long exposure)")
add_input(tab_camera, "camera_movement", "Camera movement (Pan, Tilt, Dolly, Steadicam)")
add_input(tab_camera, "background_depth", "Background depth (shallow DOF, detailed, blurred)")
add_input(tab_camera, "reflections", "Reflections & refractions (wet streets, mirrors, glass flares)")
add_input(tab_camera, "subsurface", "Subsurface scattering (light through ears, skin glow)")
add_input(tab_camera, "caustics", "Caustics (light bending through water, glass prisms)")

# Tab 4: Post-Processing
add_dropdown(tab_post, "aspect_ratio", "Aspect ratio", ["16:9", "9:16", "1:1", "4:3", "2.39:1"])
add_input(tab_post, "resolution", "Resolution & detail (e.g., 8K, 4K, 1080p, VHS)")
add_input(tab_post, "grain", "Noise / grain (film grain, digital clean, low-light noise)")
add_input(tab_post, "film_processing", "Film processing look (e.g., 35mm, vintage, iPhone)")
add_input(tab_post, "film_stock", "Film stock simulation (e.g., Kodak Portra 400, Fuji Velvia)")
add_input(tab_post, "additional_notes", "Additional notes")

# --- Action Buttons ---
button_frame = tk.Frame(outer_frame)
button_frame.pack(fill='x', pady=10)

tk.Button(button_frame, text="✨ Generate Prompt", command=generate_prompt, font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
tk.Button(button_frame, text="📋 Copy to Clipboard", command=copy_to_clipboard, font=("Helvetica", 12)).pack(side="left", padx=5)
tk.Button(button_frame, text="💾 Save Preset", command=save_preset, font=("Helvetica", 12)).pack(side="left", padx=5)
tk.Button(button_frame, text="📂 Load Preset", command=load_preset, font=("Helvetica", 12)).pack(side="left", padx=5)
tk.Button(button_frame, text="📄 Export to .txt", command=export_to_txt, font=("Helvetica", 12)).pack(side="left", padx=5)
tk.Button(button_frame, text="❌ Clear All", command=clear_all_fields, font=("Helvetica", 12)).pack(side="right", padx=5)


# --- Output Box ---
tk.Label(outer_frame, text="Generated Prompt:", font=("Helvetica", 14, "bold"), anchor="w").pack(pady=(10, 2), anchor="w")
output = scrolledtext.ScrolledText(outer_frame, height=12, wrap=tk.WORD, font=("Helvetica", 11))
output.pack(pady=2, fill="both", expand=True)

# --- Responsive behavior ---
def resize_labels(event):
    new_width = max(300, event.width - 60)
    for label in labels.values():
        if isinstance(label, tk.Label):
            label.config(wraplength=new_width)

outer_frame.bind("<Configure>", resize_labels)

root.mainloop()
