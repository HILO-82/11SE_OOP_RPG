from setuptools import setup, find_packages

setup(
    name="rpg_game",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rpg_game=rpg_game.main:main'
        ]
    }
)
