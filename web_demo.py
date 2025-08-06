"""
Simple web demo for Math Tutor Bot
Provides a web interface to test the bot functionality
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import asyncio
import json
from datetime import datetime
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Demo mode - doesn't require real API keys
DEMO_MODE = True

class DemoMathSolver:
    """Demo version of math solver for testing without API keys"""
    
    def __init__(self):
        self.demo_solutions = {
            "2+2": {
                "solution": "4",
                "steps": [
                    "This is a simple addition problem",
                    "Add 2 + 2",
                    "The result is 4"
                ],
                "problem_type": "arithmetic",
                "difficulty": "elementary"
            },
            "solve for x: 2x + 5 = 15": {
                "solution": "x = 5",
                "steps": [
                    "Start with the equation: 2x + 5 = 15",
                    "Subtract 5 from both sides: 2x = 10", 
                    "Divide both sides by 2: x = 5",
                    "Check: 2(5) + 5 = 15 ✓"
                ],
                "problem_type": "algebra",
                "difficulty": "middle_school"
            },
            "derivative of x^2": {
                "solution": "2x",
                "steps": [
                    "We need to find d/dx(x²)",
                    "Using the power rule: d/dx(xⁿ) = n·xⁿ⁻¹",
                    "For x²: n = 2",
                    "So d/dx(x²) = 2·x²⁻¹ = 2x"
                ],
                "problem_type": "calculus",
                "difficulty": "high_school"
            }
        }
    
    async def solve_problem(self, problem_text: str):
        """Demo solver that returns predefined solutions"""
        problem_lower = problem_text.lower().strip()
        
        # Check for exact matches first
        for key, solution in self.demo_solutions.items():
            if problem_lower == key.lower():
                return {
                    **solution,
                    "original_problem": problem_text,
                    "ai_provider": "demo",
                    "timestamp": datetime.now().isoformat()
                }
        
        # Check for partial matches
        for key, solution in self.demo_solutions.items():
            if any(word in problem_lower for word in key.lower().split() if len(word) > 2):
                return {
                    **solution,
                    "original_problem": problem_text,
                    "ai_provider": "demo",
                    "timestamp": datetime.now().isoformat()
                }
        
        # Default response for unknown problems
        return {
            "solution": "This is a demo version. Try: '2+2', 'solve for x: 2x + 5 = 15', or 'derivative of x^2'",
            "steps": [
                "This is a demonstration of the Math Tutor Bot",
                "The full version uses OpenAI GPT or Google Gemini",
                "Configure your API keys in .env to enable full functionality",
                "For now, try one of the demo problems above"
            ],
            "problem_type": "demo",
            "difficulty": "demo",
            "original_problem": problem_text,
            "ai_provider": "demo",
            "timestamp": datetime.now().isoformat()
        }

# Initialize demo solver
demo_solver = DemoMathSolver()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve_problem():
    """API endpoint to solve math problems"""
    try:
        data = request.get_json()
        problem = data.get('problem', '').strip()
        
        if not problem:
            return jsonify({'error': 'No problem provided'}), 400
        
        # Use async solver
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            solution = loop.run_until_complete(demo_solver.solve_problem(problem))
        finally:
            loop.close()
        
        return jsonify(solution)
        
    except Exception as e:
        logger.error(f"Error solving problem: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Math Tutor Bot Demo',
        'mode': 'demo' if DEMO_MODE else 'production',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# Create templates directory and files
def setup_templates():
    """Create HTML template for the web interface"""
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Create main HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Tutor Bot - Web Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .demo-notice {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 25px;
            color: #856404;
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .examples {
            margin-bottom: 20px;
        }
        
        .example-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .example-btn {
            background: #f8f9fa;
            color: #333;
            border: 1px solid #dee2e6;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .example-btn:hover {
            background: #e9ecef;
            transform: none;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .result {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .result h3 {
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 5px;
        }
        
        .solution {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            font-size: 18px;
            font-weight: bold;
            color: #155724;
        }
        
        .steps {
            margin-top: 15px;
        }
        
        .step {
            background: white;
            border-left: 4px solid #667eea;
            padding: 10px 15px;
            margin: 10px 0;
            border-radius: 0 5px 5px 0;
        }
        
        .metadata {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 12px;
            color: #666;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .feature {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .feature-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        @media (max-width: 600px) {
            .input-group {
                flex-direction: column;
            }
            
            .example-buttons {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Math Tutor Bot</h1>
            <p>AI-Powered Step-by-Step Math Solutions</p>
        </div>
        
        <div class="content">
            <div class="demo-notice">
                <strong>📍 Demo Mode:</strong> This is a demonstration version. Try the sample problems below, or configure your API keys in <code>.env</code> for full functionality.
            </div>
            
            <div class="input-section">
                <div class="input-group">
                    <input type="text" id="problemInput" placeholder="Enter your math problem here..." />
                    <button onclick="solveProblem()" id="solveBtn">Solve</button>
                </div>
                
                <div class="examples">
                    <p><strong>Try these examples:</strong></p>
                    <div class="example-buttons">
                        <button class="example-btn" onclick="setExample('2+2')">2+2</button>
                        <button class="example-btn" onclick="setExample('solve for x: 2x + 5 = 15')">Solve: 2x + 5 = 15</button>
                        <button class="example-btn" onclick="setExample('derivative of x^2')">Derivative of x²</button>
                        <button class="example-btn" onclick="setExample('what is 15% of 80?')">15% of 80</button>
                    </div>
                </div>
            </div>
            
            <div id="loading" class="loading" style="display: none;">
                <p>🤔 Solving your math problem...</p>
            </div>
            
            <div id="result" class="result" style="display: none;">
                <!-- Results will be inserted here -->
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">📝</div>
                    <h4>Step-by-Step</h4>
                    <p>Detailed explanations for every solution</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎥</div>
                    <h4>Video Explanations</h4>
                    <p>Educational videos (in full version)</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📸</div>
                    <h4>Image Recognition</h4>
                    <p>Solve handwritten problems (in full version)</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🤖</div>
                    <h4>AI Powered</h4>
                    <p>OpenAI GPT & Google Gemini integration</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function setExample(problem) {
            document.getElementById('problemInput').value = problem;
        }
        
        async function solveProblem() {
            const problemInput = document.getElementById('problemInput');
            const problem = problemInput.value.trim();
            
            if (!problem) {
                alert('Please enter a math problem!');
                return;
            }
            
            const solveBtn = document.getElementById('solveBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            // Show loading state
            solveBtn.disabled = true;
            solveBtn.textContent = 'Solving...';
            loading.style.display = 'block';
            result.style.display = 'none';
            
            try {
                const response = await fetch('/api/solve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ problem: problem })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    displayResult(data);
                } else {
                    throw new Error(data.error || 'Unknown error');
                }
                
            } catch (error) {
                console.error('Error:', error);
                result.innerHTML = '<div style="color: red;">Error: ' + error.message + '</div>';
                result.style.display = 'block';
            }
            
            // Reset button state
            solveBtn.disabled = false;
            solveBtn.textContent = 'Solve';
            loading.style.display = 'none';
        }
        
        function displayResult(data) {
            const result = document.getElementById('result');
            
            let html = '<h3>📋 Solution</h3>';
            html += '<div class="solution">Answer: ' + data.solution + '</div>';
            
            if (data.steps && data.steps.length > 0) {
                html += '<div class="steps"><h4>Step-by-step explanation:</h4>';
                data.steps.forEach((step, index) => {
                    html += '<div class="step"><strong>Step ' + (index + 1) + ':</strong> ' + step + '</div>';
                });
                html += '</div>';
            }
            
            html += '<div class="metadata">';
            html += '<span>Problem Type: ' + (data.problem_type || 'Unknown') + '</span>';
            html += '<span>Difficulty: ' + (data.difficulty || 'Unknown') + '</span>';
            html += '<span>AI Provider: ' + (data.ai_provider || 'Unknown') + '</span>';
            html += '</div>';
            
            result.innerHTML = html;
            result.style.display = 'block';
        }
        
        // Allow Enter key to solve
        document.getElementById('problemInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                solveProblem();
            }
        });
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w') as f:
        f.write(html_template)

if __name__ == '__main__':
    setup_templates()
    print("🌐 Starting Math Tutor Bot Web Demo...")
    print("📍 Demo Mode: Try sample problems without API keys")
    print("🔗 Open: http://localhost:8080")
    print("⚙️  Configure .env file for full functionality")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
