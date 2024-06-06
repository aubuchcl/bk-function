from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def make_output_pretty(output):
    # Decode binary data and ignore errors
    decoded_output = output.decode('utf-8', errors='ignore')
    # Split the output into lines for better readability
    lines = decoded_output.splitlines()
    pretty_lines = []

    # Filter lines to keep only high-level steps
    for line in lines:
        if line.startswith("=>"):
            pretty_lines.append(line.strip())

    # Join the filtered lines with newline characters
    pretty_output = "\n".join(pretty_lines)
    return pretty_output.strip()

@app.route('/build', methods=['POST'])
def build_container():
    data = request.json
    dockerfile_content = data.get('dockerfile')
    image_name = data.get('image_name')

    if not dockerfile_content or not image_name:
        return jsonify({'error': 'dockerfile content and image name are required'}), 400

    # Write the Dockerfile content to a file, ensuring newlines are preserved
    with open('Dockerfile', 'w') as dockerfile:
        dockerfile.write(dockerfile_content.replace("\\n", "\n"))

    # Use BuildKit to build the image
    result = subprocess.run([
        'buildctl', 'build', '--frontend', 'dockerfile.v0', 
        '--local', 'context=.', '--local', 'dockerfile=.', 
        '--output', f'type=docker,name={image_name},push=false'
    ], capture_output=True)

    if result.returncode != 0:
        stderr = make_output_pretty(result.stderr)
        return jsonify({'error': stderr}), 500

    stdout = make_output_pretty(result.stdout)

    return jsonify({'message': 'Image built successfully', 'output': stdout})

if __name__ == '__main__':
    app.run(host='::', port=5000)
