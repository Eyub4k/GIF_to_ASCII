from PIL import Image
import os
import time
import numpy as np

# Caractères ASCII optimisés pour plus de précision (du sombre au clair)
ASCII_CHARS = "@$%#&*+=|;:~-,. "

def resize_image(image, new_width=80):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)  # Réduction verticale pour lisibilité
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Algorithme de qualité

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = np.array(image)  # Convertit en tableau NumPy
    ascii_idx = pixels // 16  # Plus de niveaux (255/16 ≈ 16 caractères)
    return "".join(ASCII_CHARS[min(idx, len(ASCII_CHARS)-1)] for idx in ascii_idx.ravel())

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def precompute_frames(gif_path, new_width=80):
    gif = Image.open(gif_path)
    frames = []
    
    for frame in range(gif.n_frames):
        gif.seek(frame)
        img = gif.copy().convert("RGBA")  # Supporte la transparence
        img = resize_image(img, new_width)
        img = grayify(img)
        ascii_str = pixels_to_ascii(img)
        pixel_count = len(ascii_str)
        ascii_frame = "\n".join(ascii_str[i:i+new_width] for i in range(0, pixel_count, new_width))
        frames.append(ascii_frame)
    
    return frames, gif.n_frames

def main(gif_path, new_width=80, frame_delay=0.1):
    try:
        # Précalcule les frames une seule fois
        ascii_frames, frame_count = precompute_frames(gif_path, new_width)
        print(f"Précalcul terminé : {frame_count} frames prêtes.")
        
        # Animation optimisée
        while True:
            for ascii_frame in ascii_frames:
                clear_terminal()
                print(ascii_frame)
                time.sleep(frame_delay)
                
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    gif_path = "/path"
    main(gif_path, new_width=80, frame_delay=0.08)  
