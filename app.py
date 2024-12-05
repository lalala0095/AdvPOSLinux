import os
from app import create_app
from flask import url_for, Response
from datetime import datetime

# Create an instance of the app using the factory function
app = create_app()

def generate_sitemap(app, domain):
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Automatically retrieve routes from Flask
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and not rule.arguments:
            url = url_for(rule.endpoint, _external=True).replace("http://127.0.0.1:5000", domain)
            sitemap.append('<url>')
            sitemap.append(f'<loc>{url}</loc>')
            sitemap.append(f'<lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            sitemap.append('<changefreq>daily</changefreq>')
            sitemap.append('<priority>0.5</priority>')
            sitemap.append('</url>')

    sitemap.append('</urlset>')
    return ''.join(sitemap)

@app.route('/sitemap.xml')
def sitemap():
    sitemap_content = generate_sitemap(app, domain="https://advposapp.com")
    return Response(sitemap_content, mimetype='application/xml')

@app.route('/sitemap_static.xml')
def sitemap_static():
    return app.send_static_file('sitemap_static.xml')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# # local testing
# if __name__ == "__main__":
#     app.run(debug=True)
