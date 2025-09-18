# ---------- Video Prompt Generator ----------

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import platform
import json

# --- Core Functions ---

def get_widget_value(widget):
    """Gets the value from a ScrolledText widget."""
    return widget.get("1.0", tk.END).strip()

def set_widget_value(widget, value):
    """Sets the value of a ScrolledText widget."""
    widget.delete("1.0", tk.END)
    widget.insert("1.0", value)

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

canvas = tk.Canvas(main_frame, highlightthickness=0) # Remove canvas border
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
title_label = ttk.Label(outer_frame, text="AI Prompt Generator", style="Title.TLabel", padding=(10, 10))
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
    box = scrolledtext.ScrolledText(parent, height=height, wrap=tk.WORD, font=("Helvetica", 11), relief="solid", borderwidth=1)
    box.pack(pady=2, anchor="w", fill="x", expand=True)
    boxes[key] = box
    return box

# --- Input Fields ---
# (Content is identical to previous version, omitted for brevity)
add_input(tab_scene, "realism", "Realism level (Photo Realistic, painterly, cartoon, stylized)")
add_input(tab_scene, "emotional_theme", "Describe the emotional theme (joy, fear, love, tension)")
add_input(tab_scene, "mood", "Mood & style (dark, playful, suspenseful, whimsical)")
add_input(tab_scene, "cultural", "Cultural influence (cyberpunk Tokyo, Afrofuturism, Mayan temples)")
add_input(tab_scene, "scene_details", "Describe the scene (location, environment, landscape, single or group of people)")
add_input(tab_scene, "environment", "Describe the environment and setting (architecture, materials, vibe)")
add_input(tab_scene, "imperfections", "Describe the environment imperfections (scratches, dust, chipped paint)")
add_input(tab_scene, "time_of_day", "Time of day (dawn, golden hour, twilight, midnight)")
add_input(tab_scene, "season", "Season or climate (spring bloom, autumn leaves, summer heat, winter cold)")
add_input(tab_scene, "lighting", "Describe lighting & weather (soft, harsh, natural, artificial)")
add_input(tab_scene, "scene_materials", "Describe materials & textures in the scene (stained concrete, velvet, rough leather)")
add_input(tab_scene, "atmosphere", "Describe the atmosphere (haze, fog, smoke, underwater, dust)")
add_input(tab_scene, "color_palette", "Color palette (60/30/10 rule, color harmony, tone)")

add_input(tab_subject, "character_details", "Describe the characters (emotions, props, context)")
add_input(tab_subject, "gender", "Gender (male, female, androgynous)")
add_input(tab_subject, "ethnicity", "Ethnicity (Chinese, Indian, Nigerian, Italian, etc.)")
add_input(tab_subject, "age", "Age Specificity (toddler, teenager, mid-30s, elderly)")
add_input(tab_subject, "pose_body", "Pose & Body Language (standing tall, slouched, walking, fighting, dancing)")
add_input(tab_subject, "body_type", "Body Type (slim, obese, muscular, athletic)")
add_input(tab_subject, "hands_gestures", "Hands & Gestures (open palms, gripping object, hidden, expressive)")
add_input(tab_subject, "eyes", "Describe the eyes (color, expression, gaze direction)")
add_input(tab_subject, "skin", "Describe the skin in detail(tone, texture, imperfections, makeup (very important step))")
add_input(tab_subject, "mouth", "Describe the mouth (shape, fullness, emotion)")
add_input(tab_subject, "hair", "Describe the hair (color, thickness, style, length)")
add_input(tab_subject, "clothing", "Describe the clothing (style, color palette, texture, brand, imperfections)")

add_input(tab_camera, "director_shot_by", "Director / Cinematographer Pair:\n\n[Examples...]", height=10)
add_input(tab_camera, "camera_angle", "Describe camera angle and framing (worm’s-eye, wide shot, close-up)")
add_input(tab_camera, "framing", "Framing style (center frame, leading lines, frame-in-frame)")
add_input(tab_camera, "lens", "Lens details (12mm wide, 50mm natural, f-stop for bokeh)")
add_input(tab_camera, "camera_model", "Camera model/sensor type (ARRI Alexa, RED Komodo, Leica M10)")
add_input(tab_camera, "focus_depth", "Focus depth (macro detail, shallow focus, deep focus)")
add_input(tab_camera, "shutter_speed", "Shutter speed / motion (motion blur, frozen action, long exposure)")
add_input(tab_camera, "camera_movement", "Describe the overall camera movement (Pan, Tilt, Dolly)")
add_input(tab_camera, "background_depth", "Background depth (shallow DOF, detailed, blurred)")
add_input(tab_camera, "reflections", "Describe reflections & refractions (wet streets, mirrors, glass flares)")
add_input(tab_camera, "subsurface", "Describe subsurface scattering (light through ears, glow under skin)")
add_input(tab_camera, "caustics", "Describe caustics (light bending through water, glass prisms)")

add_input(tab_post, "aspect_ratio", "Aspect ratio (Type: final image should be cropped to ... 16:9, 9:16, IMAX)")
add_input(tab_post, "resolution", "Resolution & detail level (8K cinematic, VHS grainy)")
add_input(tab_post, "grain", "Noise / grain (film grain, digital clean, noisy low-light)")
add_input(tab_post, "film_processing", "Film processing look (35mm, vintage, iPhone aesthetic)")
add_input(tab_post, "film_stock", "Film stock simulation (Kodak Portra 400, Fuji Velvia, Ilford HP5)")
add_input(tab_post, "additional_notes", "Add any additional notes")


# --- Action Buttons ---
button_frame = ttk.Frame(outer_frame)
button_frame.pack(fill='x', padx=10, pady=10)

ttk.Button(button_frame, text="✨ Generate Prompt", command=generate_prompt, style="Bold.TButton").pack(side="left", padx=5)
ttk.Button(button_frame, text="📋 Copy", command=copy_to_clipboard).pack(side="left", padx=5)
ttk.Button(button_frame, text="💾 Save", command=save_preset).pack(side="left", padx=5)
ttk.Button(button_frame, text="📂 Load", command=load_preset).pack(side="left", padx=5)
ttk.Button(button_frame, text="📄 Export", command=export_to_txt).pack(side="left", padx=5)
ttk.Button(button_frame, text="❌ Clear All", command=clear_all_fields).pack(side="right", padx=5)

# --- Output Box ---
output_frame = ttk.Frame(outer_frame)
output_frame.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(output_frame, text="Generated Prompt:", style="Header.TLabel").pack(pady=(5, 2), anchor="w")
output = scrolledtext.ScrolledText(output_frame, height=12, wrap=tk.WORD, font=("Helvetica", 11), relief="solid", borderwidth=1)
output.pack(pady=2, fill="both", expand=True)

root.mainloop()
