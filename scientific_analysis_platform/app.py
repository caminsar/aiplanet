from flask import Flask, render_template, request, jsonify
import os

# Import the research assistant
from research_assistant.assistant_core import ResearchAssistant

# Determine the correct template folder path
# Assuming app.py is in scientific_analysis_platform/
# and templates are in scientific_analysis_platform/visualization/templates/
# We might need a general templates folder if assistant has its own pages
visualization_template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visualization', 'templates')
visualization_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visualization', 'static')

# For now, let's assume assistant pages can also go into visualization/templates or a new top-level 'templates'
# For simplicity, using the existing one, but this might need adjustment for larger apps.
app = Flask(__name__, template_folder=visualization_template_dir, static_folder=visualization_static_dir)

# Initialize the Research Assistant
# In a real app, KG querier and document store would be properly initialized and passed
research_assistant_instance = ResearchAssistant(kg_querier=None, document_store=None)


@app.route('/')
def hello_world():
    # Use a template for the home page as well for consistency
    return render_template('index.html', title='Welcome')

@app.route('/visualization')
def visualization_home():
    return render_template('visualization_home.html', title='Visualization Hub')

@app.route('/visualization/map_placeholder')
def map_placeholder_page():
    return render_template('map_placeholder.html', title='Map Placeholder')

@app.route('/visualization/chart_placeholder')
def chart_placeholder_page():
    return render_template('chart_placeholder.html', title='Chart Placeholder')

# --- Research Assistant Routes ---
@app.route('/assistant', methods=['GET', 'POST'])
def assistant_page():
    query = ""
    response = None
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            response = research_assistant_instance.process_query(query)
    elif request.method == 'GET':
        query = request.args.get('query', '')
        if query:
            response = research_assistant_instance.process_query(query)

    return render_template('assistant_page.html', title='Research Assistant', query=query, response=response)

@app.route('/api/assistant/query', methods=['POST'])
def assistant_api_query():
    if not request.json or 'query' not in request.json:
        return jsonify({"error": "Missing 'query' in JSON payload"}), 400

    query_text = request.json['query']
    response_data = research_assistant_instance.process_query(query_text)
    return jsonify(response_data)


if __name__ == '__main__':
    print(f"Looking for templates in: {app.template_folder}")
    print(f"Looking for static files in: {app.static_folder}")
    # Create a dummy index.html if it doesn't exist for the new home route
    if not os.path.exists(os.path.join(app.template_folder, 'index.html')):
        try:
            with open(os.path.join(app.template_folder, 'index.html'), 'w') as f:
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
        <li><a href="{{ url_for('visualization_home') }}">Visualization Hub</a></li>
        <li><a href="{{ url_for('assistant_page') }}">Research Assistant</a></li>
    </ul></nav>
    <main><h2>Welcome!</h2><p>This is the main entry point to the platform.</p></main>
    <footer><p>&copy; 2023 Scientific Analysis Platform</p></footer>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body></html>""")
            print("Created dummy index.html")
        except Exception as e:
            print(f"Could not create dummy index.html: {e}")

    app.run(debug=True, host='0.0.0.0', port=5000)
