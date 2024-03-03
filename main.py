import photon
from photon import Theme, Colors

from routes import index, root


app = photon.Photon(root=root.Root)



PAGES = [index.Index(app)]

for page in PAGES:
    app.register_page(page)

app.open("Index")

app.run()