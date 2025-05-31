import os
from flask import Flask, render_template, request, redirect, send_from_directory

app = Flask(__name__)

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Company options
COMPANIES = ["SunCoke Energy", "Teine Energy"]

@app.route("/", methods=["GET", "POST"])
def generate_presentation():
    # Show company selection form
    if request.method == "GET":
        return render_template('index.html', companies=COMPANIES)
    
    # Handle form submission
    if request.method == "POST":
        company = request.form.get("company")
        
        if not company:
            return render_template('index.html', error="Please select a company", companies=COMPANIES)
        
        # Redirect to presentation with company parameter
        if company == "SunCoke Energy":
            return redirect("/index.html?company=suncoke")
        elif company == "Teine Energy":
            return redirect("/index.html?company=teine")
        else:
            return redirect("/index.html")

# Static file serving
@app.route('/index.html')
def serve_presentation():
    return send_from_directory('..', 'index.html')

@app.route('/dist/<path:filename>')
def serve_dist(filename):
    return send_from_directory('../dist', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('../css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../js', filename)

@app.route('/presentation-slides/<path:filename>')
def serve_slides(filename):
    return send_from_directory('../presentation-slides', filename)

@app.route('/img/<path:filename>')
def serve_images(filename):
    return send_from_directory('../img', filename)

@app.route('/media/<path:filename>')
def serve_media(filename):
    return send_from_directory('../media', filename)

@app.route('/plugin/<path:filename>')
def serve_plugins(filename):
    return send_from_directory('../plugin', filename)

@app.route('/css/suncoke/<path:filename>')
def serve_suncoke_css(filename):
    return send_from_directory('../css/suncoke', filename)

@app.route('/css/teine/<path:filename>')
def serve_teine_css(filename):
    return send_from_directory('../css/teine', filename)

@app.route('/css/custom/<path:filename>')
def serve_custom_css(filename):
    return send_from_directory('../css/custom', filename)

@app.route('/MikaelChallenge/<path:filename>')
def serve_mikael_challenge(filename):
    return send_from_directory('../MikaelChallenge', filename)

if __name__ == "__main__":
    app.run(debug=True)