import photon
from photon import Theme, Colors

from routes import index, root


app = photon.Photon(root=root.Root)



PAGES = [index.Index(app)]

for page in PAGES:
    app.register_page(page)

@app.event("on_init")
def on_init():
    app.open("Index")

@app.event("on_error")
def on_error(source, message):
    print(f"Error message from {type(source).__name__}: {message}")

app.run()