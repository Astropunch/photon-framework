import photon

from routes import index, about


app = photon.Photon()

PAGES = [index.Index(app), about.About(app)]

for page in PAGES:
    app.register_page(page)

app.open("Index")    

app.run()