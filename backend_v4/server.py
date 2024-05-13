from flask import Flask, request, jsonify
import API_helper
import config

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_project():
    data = request.json
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        # Extract parameters from the request
        clone_path = data.get('path')
        owner = data.get('owner')
        repo_name = data.get('repo_name')
        github_token = data.get('github_token', config.GITHUB_TOKEN)  # Default to token from config if not provided
        method_id = data.get('method_id', 3)  # Default method is 3 if not provided

        # Call the API function
        result = API_helper.API(clone_path, owner, repo_name, github_token, method_id)
        print(result)

        # Return the results as JSON
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()  # This prints the full stack trace
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == '__main__':
    app.run(debug=True)
