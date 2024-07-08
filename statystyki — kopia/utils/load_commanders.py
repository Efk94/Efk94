def load_commanders():
    avatar_folder = os.path.join(os.path.dirname(__file__), 'Avatar')  # Użyj względnej ścieżki
    commanders = {}
    for filename in os.listdir(avatar_folder):
        name, _ = os.path.splitext(filename)
        commanders[name] = os.path.join(avatar_folder, filename)
    return commanders
