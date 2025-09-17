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
            formatted_key = key.replace('_', ' ').title()
            prompt_lines.append(f"- {formatted_key}: {value}")

    if prompt_lines:
        final_prompt = "Merge the following answers into a single descriptive paragraph...\n\n" + "\n".join(prompt_lines)
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
    if messagebox.askokcancel("Clear All", "Are you sure you want to clear all fields?"):
        for widget in boxes.values():
            set_widget_value(widget, "")
        output.delete("1.0", tk.END)

def save_preset():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        title="Save Preset As"
    )
    if not filepath: return

    preset_data = {key: get_widget_value(widget) for key, widget in boxes.items()}

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(preset_data, f, indent=4)
        messagebox.showinfo("Success", "Preset saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save preset file.\nError: {e}")

def load_preset():
    filepath = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        title="Load Preset"
    )
    if not filepath: return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            preset_data = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load preset file.\nError: {e}")
        return

    for key, value in preset_data.items():
        if key in boxes:
            set_widget_value(boxes[key], value)
    messagebox.showinfo("Success", "Preset loaded successfully!")

def export_to_txt():
    prompt_content = output.get("1.0", tk.END).strip()
    if not prompt_content:
        messagebox.showwarning("Empty Prompt", "The generated prompt is empty.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Export Prompt As"
    )
    if not filepath: return

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

# --- Theming ---
style = ttk.Style(root)
# Use the default theme for the OS
theme = style.theme_use()
style.configure('.', font=("Helvetica", 11))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("Title.TLabel", font=("Helvetica", 24, "bold"))
style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))
style.configure("TButton", font=("Helvetica", 12))
style.configure("Bold.TButton", font=("Helvetica", 12, "bold"))


# --- Main Scrolling Canvas ---
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame)
scroll_y = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
outer_frame = ttk.Frame(canvas)

outer_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=outer_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

boxes = {}

def _on_mousewheel(event):
    if platform.system() == "Windows":
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    else:
        if event.num == 4: canvas.yview_scroll(-1, "units")
        elif event.num == 5: canvas.yview_scroll(1, "units")
        else: canvas.yview_scroll(int(-1 * event.delta), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# --- UI Elements ---
title_label = ttk.Label(outer_frame, text="AI Prompt Generator", style="Title.TLabel")
title_label.pack(pady=(10, 20))

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

def add_input(parent, key, label_text, height=3):
    label = ttk.Label(parent, text=label_text)
    label.pack(pady=(5,2), anchor="w", fill="x")
    box = scrolledtext.ScrolledText(parent, height=height, wrap=tk.WORD, font=("Helvetica", 11))
    box.pack(pady=2, anchor="w", fill="x", expand=True)
    boxes[key] = box
    return box

def add_dropdown(parent, key, label_text, options):
    label = ttk.Label(parent, text=label_text)
    label.pack(pady=(5,2), anchor="w", fill="x")
    combo = ttk.Combobox(parent, values=options, state="readonly")
    combo.pack(pady=2, anchor="w", fill="x", expand=True)
    boxes[key] = combo
    return combo

director_options = ["Spielberg & Kamiński", "Nolan & Hoytema", "Scorsese & Ballhaus", "Tarantino & Richardson", "Anderson & Yeoman", "Fincher & Cronenweth", "Villeneuve & Deakins", "Villeneuve & Fraser", "Iñárritu & Lubezki", "Malick & Almendros", "Aronofsky & Libatique"]

# --- Input Fields ---
add_dropdown(tab_scene, "realism", "Realism level", ["Photo Realistic", "Painterly", "Cartoon", "Stylized"])
add_input(tab_scene, "emotional_theme", "Emotional theme")
add_dropdown(tab_scene, "mood", "Mood & style", ["Dark", "Playful", "Suspenseful", "Whimsical", "Romantic", "Eerie"])
add_input(tab_scene, "cultural", "Cultural influence")
add_input(tab_scene, "scene_details", "Scene description")
add_input(tab_scene, "environment", "Environment & setting")
add_input(tab_scene, "imperfections", "Environment imperfections")
add_dropdown(tab_scene, "time_of_day", "Time of day", ["Dawn", "Golden Hour", "High Noon", "Twilight", "Midnight"])
add_dropdown(tab_scene, "season", "Season or climate", ["Spring", "Summer", "Autumn", "Winter"])
add_input(tab_scene, "lighting", "Lighting & weather")
add_input(tab_scene, "scene_materials", "Materials & textures")
add_input(tab_scene, "atmosphere", "Atmosphere")
add_input(tab_scene, "color_palette", "Color palette")

add_input(tab_subject, "character_details", "Character description")
add_dropdown(tab_subject, "gender", "Gender", ["Male", "Female", "Androgynous", "Non-binary"])
add_input(tab_subject, "ethnicity", "Ethnicity")
add_input(tab_subject, "age", "Age")
add_input(tab_subject, "pose_body", "Pose & Body Language")
add_input(tab_subject, "body_type", "Body Type")
add_input(tab_subject, "hands_gestures", "Hands & Gestures")
add_input(tab_subject, "eyes", "Eyes")
add_input(tab_subject, "skin", "Skin")
add_input(tab_subject, "mouth", "Mouth")
add_input(tab_subject, "hair", "Hair")
add_input(tab_subject, "clothing", "Clothing")

add_dropdown(tab_camera, "director_shot_by", "Director / Cinematographer Style", director_options)
add_input(tab_camera, "camera_angle", "Camera angle")
add_dropdown(tab_camera, "framing", "Framing style", ["Center Frame", "Leading Lines", "Rule of Thirds", "Frame-in-Frame"])
add_input(tab_camera, "lens", "Lens details")
add_input(tab_camera, "camera_model", "Camera model/sensor")
add_input(tab_camera, "focus_depth", "Focus depth")
add_input(tab_camera, "shutter_speed", "Shutter speed / motion")
add_input(tab_camera, "camera_movement", "Camera movement")
add_input(tab_camera, "background_depth", "Background depth")
add_input(tab_camera, "reflections", "Reflections & refractions")
add_input(tab_camera, "subsurface", "Subsurface scattering")
add_input(tab_camera, "caustics", "Caustics")

add_dropdown(tab_post, "aspect_ratio", "Aspect ratio", ["16:9", "9:16", "1:1", "4:3", "2.39:1"])
add_input(tab_post, "resolution", "Resolution & detail")
add_input(tab_post, "grain", "Noise / grain")
add_input(tab_post, "film_processing", "Film processing look")
add_input(tab_post, "film_stock", "Film stock simulation")
add_input(tab_post, "additional_notes", "Additional notes")

# --- Action Buttons ---
button_frame = ttk.Frame(outer_frame)
button_frame.pack(fill='x', pady=20)

ttk.Button(button_frame, text="✨ Generate Prompt", command=generate_prompt, style="Bold.TButton").pack(side="left", padx=5)
ttk.Button(button_frame, text="📋 Copy", command=copy_to_clipboard).pack(side="left", padx=5)
ttk.Button(button_frame, text="💾 Save", command=save_preset).pack(side="left", padx=5)
ttk.Button(button_frame, text="📂 Load", command=load_preset).pack(side="left", padx=5)
ttk.Button(button_frame, text="📄 Export", command=export_to_txt).pack(side="left", padx=5)
ttk.Button(button_frame, text="❌ Clear All", command=clear_all_fields).pack(side="right", padx=5)

# --- Output Box ---
ttk.Label(outer_frame, text="Generated Prompt:", style="Header.TLabel").pack(pady=(10, 2), anchor="w")
output = scrolledtext.ScrolledText(outer_frame, height=12, wrap=tk.WORD, font=("Helvetica", 11))
output.pack(pady=2, fill="both", expand=True)

root.mainloop()
