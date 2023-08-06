# Brython-components

Brython-components is an easy implementation of brython's webcomonent.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install brip
brip install brython-components
```

## Usage

'''python
from brython_components impoprt defineElement, customElement

@defineElement("bold-italic")
class BoldItalic(customElement):
    def connectedCallback(self):
        super().connectedCallback()
        print("connected callback", self)

    def render(self):
        return f"<b><i>{self.attrs['data-val']}</i></b>"
'''

## License

[MIT](https://choosealicense.com/licenses/mit/)
