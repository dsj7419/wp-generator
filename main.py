from settings.settings import Settings
from generators.space import Space

def main():
    settings = Settings()
    space = Space(settings)
    space.generate()

if __name__ == "__main__":
    main()