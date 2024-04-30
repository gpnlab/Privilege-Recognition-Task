import sys
import os


class EXE:
    def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


# example of loading img
# asset_url = resource_path('assets/chars/hero.png')
# hero_asset = pygame.image.load(asset_url)s
