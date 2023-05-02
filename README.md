# pyckaxe

Python package to speed up web scraper development.

Currently this project follows this pattern

```
|── .env/
|── README.md
├── pyproject.toml
├── src/
|   |── project_name/
│   |    ├── __init__.py
│   |    ├── __main__.py
│   |    |── base.py
│   |    |── core.py
│   |    |── data.py
│   |    └── utils.py
|   |── app.py
|   |── cli.py
|   |── gui.py
|   └── settings.py
└── tests/
    └── __init__.py
```

Here, `app.py`, `cli.py` and `gui.py` are just for local testing, experimenting and future development, and should not be suggested any changes.

## Installation

```bash
$ pip install pyckaxe
```

## Usage

- <spam style='color: red;'>TODO</spam>

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pyckaxe` was created by Vagner Bessa. Vagner Bessa retains all rights to the source and it may not be reproduced, distributed, or used to create derivative works.

## Credits

`pyckaxe` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
