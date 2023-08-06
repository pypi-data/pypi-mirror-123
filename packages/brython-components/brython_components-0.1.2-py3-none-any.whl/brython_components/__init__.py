from browser import html, webcomponent


def defineElement(name):
    def define(cls):
        webcomponent.define(name, cls)
        return cls

    return define


class customElement:
    def __init__(self):
        self.renderRoot = self.createRenderRoot()

    def createRenderRoot(self):
        return self.attachShadow({"mode": "open"})

    def connectedCallback(self):
        self.renderRoot.appendChild(html.STYLE(self.styles()))
        self.renderRoot.appendChild(
            html.TEMPLATE(self.render()).content.cloneNode(True)
        )

    def styles(self):
        return ""

    def render(self):
        return ""
