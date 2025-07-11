from flask import Flask, render_template, request, jsonify
import os
import datetime # For providing 'now' to templates if needed for footer year

# Import application components
from research_assistant.assistant_core import ResearchAssistant
from data_management.api_routes import data_api_bp
from visualization.routes import visualization_bp # Import the new visualization blueprint

# --- Application Setup ---
def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # Assuming all templates and static files are primarily managed by the visualization blueprint's settings
    # or a general app-level templates/static folder if that was the chosen structure.
    # The visualization_bp is set up to use 'visualization/templates' and 'visualization/static'.
    # If other blueprints need their own, they should specify their template_folder.
    # For app-level templates like index.html, if not covered by a blueprint,
    # Flask's default is a 'templates' folder in the app root.
    # Let's ensure Flask app itself also knows where to find general templates if needed.
    # For this structure, 'visualization/templates' is acting as the main template hub.
    template_dir = os.path.join(base_dir, 'visualization', 'templates')
    static_dir = os.path.join(base_dir, 'visualization', 'static') # This is also what visualization_bp uses

    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)

    _app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    _app.research_assistant_instance = ResearchAssistant(kg_querier=None, document_store=None)

    # Register Blueprints
    _app.register_blueprint(data_api_bp)
    _app.register_blueprint(visualization_bp) # Register the visualization blueprint

    # Context processor to make 'now' available to all templates for the year in footer
    @_app.context_processor
    def inject_now():
        return {'now': datetime.datetime.utcnow()}

    # --- Core Application Routes ---
    # (Routes previously directly under /visualization/* are now in visualization_bp with /view/* prefix)
    # (Routes for /assistant and /api/assistant remain here, or could be moved to their own blueprint)

    @_app.route('/')
    def hello_world(): # This is the homepage
        return render_template('index.html', title='Welcome')

    # --- Research Assistant Routes (Consider moving to a Blueprint later) ---
    # For now, keeping them here. If they grow, a 'assistant_bp' would be good.
    @_app.route('/assistant', methods=['GET', 'POST'])
    def assistant_page():
        query = ""
        response = None
        if request.method == 'POST':
            query = request.form.get('query', '')
            if query:
                response = _app.research_assistant_instance.process_query(query)
        elif request.method == 'GET':
            query = request.args.get('query', '')
            if query:
                response = _app.research_assistant_instance.process_query(query)
        return render_template('assistant_page.html', title='Research Assistant', query=query, response=response)

    @_app.route('/api/assistant/query', methods=['POST'])
    def assistant_api_query():
        if not request.json or 'query' not in request.json:
            return jsonify({"error": "Missing 'query' in JSON payload"}), 400
        query_text = request.json['query']
        response_data = _app.research_assistant_instance.process_query(query_text)
        return jsonify(response_data)

    return _app

app = create_app()

if __name__ == '__main__':
    print(f"Looking for templates in: {app.template_folder}")
    print(f"Looking for static files in: {app.static_folder}")

    index_html_path = os.path.join(app.template_folder, 'index.html')
    if not os.path.exists(index_html_path):
        try:
            with open(index_html_path, 'w') as f:
                # Updated nav to reflect blueprint paths
                f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome - Scientific Analysis Platform</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header><h1>Scientific Analysis Platform</h1></header>
    <nav><ul>
        <li><a href="{{ url_for('hello_world') }}">Home</a></li>
        <li><a href="{{ url_for('visualization_bp.home') }}">Visualization Hub</a></li>
        <li><a href="{{ url_for('visualization_bp.data_catalog_page') }}">Data Catalog</a></li>
        <li><a href="{{ url_for('assistant_page') }}">Research Assistant</a></li>
        <li><a href="{{ url_for('data_api.list_stations') }}">Stations API</a></li>
    </ul></nav>
    <main><h2>Welcome!</h2><p>This is the main entry point to the platform. Check out the <a href="{{ url_for('data_api.health_check') }}">Data API Health</a>.</p></main>
    <footer><p>&copy; {{ now.year }} Scientific Analysis Platform</p></footer>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body></html>""")
            print(f"Created dummy index.html at {index_html_path}")
        except Exception as e:
            print(f"Could not create dummy index.html at {index_html_path}: {e}")

    app.run(debug=True, host='0.0.0.0', port=5000)
