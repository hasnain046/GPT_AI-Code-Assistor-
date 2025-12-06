from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import tempfile
import os
import sys

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if language == 'python':
            return execute_python(code)
        elif language == 'javascript':
            return execute_javascript(code)
        elif language == 'java':
            return execute_java(code)
        elif language == 'cpp':
            return execute_cpp(code)
        else:
            return jsonify({'success': False, 'error': 'Unsupported language'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def execute_python(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        result = subprocess.run([sys.executable, temp_file], 
                              capture_output=True, text=True, timeout=10)
        
        os.unlink(temp_file)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        })
            
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Code execution timed out'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def execute_javascript(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        result = subprocess.run(['node', temp_file], 
                              capture_output=True, text=True, timeout=10)
        
        os.unlink(temp_file)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        })
            
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Code execution timed out'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def execute_java(code):
    try:
        temp_dir = tempfile.mkdtemp()
        java_file = os.path.join(temp_dir, 'Main.java')
        
        with open(java_file, 'w') as f:
            f.write(code)
        
        compile_result = subprocess.run(['javac', java_file], 
                                      capture_output=True, text=True, timeout=10)
        
        if compile_result.returncode != 0:
            return jsonify({
                'success': False,
                'output': '',
                'error': compile_result.stderr
            })
        
        result = subprocess.run(['java', '-cp', temp_dir, 'Main'], 
                              capture_output=True, text=True, timeout=10)
        
        for file in os.listdir(temp_dir):
            os.unlink(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Code execution timed out'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def execute_cpp(code):
    try:
        temp_dir = tempfile.mkdtemp()
        cpp_file = os.path.join(temp_dir, 'main.cpp')
        exe_file = os.path.join(temp_dir, 'main.exe')
        
        with open(cpp_file, 'w') as f:
            f.write(code)
        
        compile_result = subprocess.run(['g++', cpp_file, '-o', exe_file], 
                                      capture_output=True, text=True, timeout=10)
        
        if compile_result.returncode != 0:
            return jsonify({
                'success': False,
                'output': '',
                'error': compile_result.stderr
            })
        
        result = subprocess.run([exe_file], 
                              capture_output=True, text=True, timeout=10)
        
        for file in os.listdir(temp_dir):
            os.unlink(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Code execution timed out'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/debug', methods=['POST'])
def debug_code():
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        debug_info = {
            'language': language,
            'lines': len(code.split('\n')),
            'characters': len(code),
            'suggestions': []
        }
        
        if language == 'python':
            debug_info['suggestions'] = debug_python(code)
        elif language == 'javascript':
            debug_info['suggestions'] = debug_javascript(code)
        elif language == 'java':
            debug_info['suggestions'] = debug_java(code)
        elif language == 'cpp':
            debug_info['suggestions'] = debug_cpp(code)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def debug_python(code):
    suggestions = []
    if 'print(' not in code:
        suggestions.append('Consider adding print statements for debugging')
    if 'def ' in code and 'return' not in code:
        suggestions.append('Functions should have return statements')
    if code.count('(') != code.count(')'):
        suggestions.append('Check parentheses balance')
    return suggestions

def debug_javascript(code):
    suggestions = []
    if 'console.log(' not in code:
        suggestions.append('Consider adding console.log for debugging')
    if 'function' in code and 'return' not in code:
        suggestions.append('Functions should have return statements')
    if code.count('{') != code.count('}'):
        suggestions.append('Check braces balance')
    return suggestions

def debug_java(code):
    suggestions = []
    if 'System.out.println(' not in code:
        suggestions.append('Consider adding print statements for debugging')
    if 'public class' not in code:
        suggestions.append('Java code should be in a public class')
    if 'public static void main' not in code:
        suggestions.append('Add main method for execution')
    return suggestions

def debug_cpp(code):
    suggestions = []
    if '#include' not in code:
        suggestions.append('Include necessary header files')
    if 'cout' not in code and 'printf' not in code:
        suggestions.append('Consider adding output statements for debugging')
    if 'int main' not in code:
        suggestions.append('Add main function for execution')
    return suggestions

if __name__ == '__main__':
    print("🚀 GPT-4o Code Assessor API Starting...")
    print("📡 Available endpoints:")
    print("   POST /execute - Execute code")
    print("   POST /debug - Debug analysis")
    print("🌐 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)