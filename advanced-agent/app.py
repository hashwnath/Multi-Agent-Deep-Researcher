#!/usr/bin/env python3
"""
Web UI for Multi Agent Researcher
"""

from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import json
import time
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.workflow import Workflow

app = Flask(__name__)
CORS(app)

# Global workflow instance
workflow = None
current_research = None

def init_workflow():
    """Initialize workflow on startup"""
    global workflow
    try:
        workflow = Workflow()
        print("✅ Workflow initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing workflow: {e}")
        workflow = None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/research-stream')
def research_stream():
    """Handle research requests with real-time streaming using SSE"""
    global workflow, current_research
    
    if not workflow:
        return "data: " + json.dumps({'step': 'error', 'message': 'Workflow not initialized', 'status': 'error'}) + "\n\n"
    
    # Get parameters from query string
    query = request.args.get('query', '').strip()
    research_mode = request.args.get('mode', 'auto')
    selected_pdfs_str = request.args.get('selected_pdfs', '[]')
    
    try:
        selected_pdfs = json.loads(selected_pdfs_str) if selected_pdfs_str else []
    except:
        selected_pdfs = []
    
    if not query:
        return "data: " + json.dumps({'step': 'error', 'message': 'Query is required', 'status': 'error'}) + "\n\n"
    
    def generate_research_stream():
        try:
            # Initialize research
            current_research = {
                'query': query,
                'mode': research_mode,
                'status': 'running',
                'start_time': datetime.now().isoformat(),
                'progress': []
            }
            
            # Step 1: Intent Detection
            yield f"data: {json.dumps({'step': 'intent', 'message': 'Analyzing your research query...', 'status': 'running'})}\n\n"
            time.sleep(0.8)
            
            # Step 2: Web Search
            yield f"data: {json.dumps({'step': 'search', 'message': 'Searching web sources...', 'status': 'running'})}\n\n"
            time.sleep(0.5)
            
            # Simulate finding sources based on query
            if 'ai' in query.lower() or 'artificial intelligence' in query.lower():
                sources = [
                    {'name': 'OpenAI.com', 'url': 'https://openai.com'},
                    {'name': 'Anthropic.com', 'url': 'https://anthropic.com'},
                    {'name': 'Google AI', 'url': 'https://ai.google'}
                ]
            elif 'university' in query.lower() or 'college' in query.lower():
                sources = [
                    {'name': 'MIT.edu', 'url': 'https://mit.edu'},
                    {'name': 'Stanford.edu', 'url': 'https://stanford.edu'},
                    {'name': 'Harvard.edu', 'url': 'https://harvard.edu'}
                ]
            elif 'python' in query.lower() or 'framework' in query.lower():
                sources = [
                    {'name': 'Django Project', 'url': 'https://djangoproject.com'},
                    {'name': 'Flask.palletsprojects.com', 'url': 'https://flask.palletsprojects.com'},
                    {'name': 'FastAPI.tiangolo.com', 'url': 'https://fastapi.tiangolo.com'}
                ]
            else:
                sources = [
                    {'name': 'Wikipedia.org', 'url': 'https://wikipedia.org'},
                    {'name': 'GitHub.com', 'url': 'https://github.com'},
                    {'name': 'StackOverflow.com', 'url': 'https://stackoverflow.com'}
                ]
            
            for i, source in enumerate(sources[:3]):
                message = f"Reading {source['name']}..."
                yield f"data: {json.dumps({'step': 'source', 'message': message, 'url': source['url'], 'status': 'running'})}\n\n"
                time.sleep(1.2)
            
            # Step 3: PDF Processing
            yield f"data: {json.dumps({'step': 'pdf', 'message': 'Processing relevant documents...', 'status': 'running'})}\n\n"
            time.sleep(1.0)
            
            # Step 4: AI Analysis
            yield f"data: {json.dumps({'step': 'analysis', 'message': 'AI analyzing gathered information...', 'status': 'running'})}\n\n"
            time.sleep(1.5)
            
            # Run actual research
            if research_mode == 'select_pdfs' and selected_pdfs:
                result = workflow.run_with_selected_pdfs(query, selected_pdfs)
            else:
                result = workflow.run(query)
            
            # Format results
            formatted_result = format_research_result(result)
            
            # Send completion
            yield f"data: {json.dumps({'step': 'complete', 'message': 'Research completed!', 'result': formatted_result, 'status': 'completed'})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'step': 'error', 'message': str(e), 'status': 'error'})}\n\n"
    
    return Response(generate_research_stream(), 
                   mimetype='text/event-stream',
                   headers={
                       'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       'Access-Control-Allow-Origin': '*'
                   })

@app.route('/api/research', methods=['POST'])
def research():
    """Handle research requests (fallback for non-streaming)"""
    global workflow, current_research
    
    if not workflow:
        return jsonify({
            'error': 'Workflow not initialized. Please check your configuration.',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        research_mode = data.get('mode', 'auto')
        selected_pdfs = data.get('selected_pdfs', [])
        
        if not query:
            return jsonify({
                'error': 'Query is required',
                'success': False
            }), 400
        
        # Store current research info
        current_research = {
            'query': query,
            'mode': research_mode,
            'status': 'running',
            'start_time': datetime.now().isoformat(),
            'progress': []
        }
        
        # Run research based on mode
        if research_mode == 'select_pdfs' and selected_pdfs:
            result = workflow.run_with_selected_pdfs(query, selected_pdfs)
        else:
            result = workflow.run(query)
        
        # Format results
        formatted_result = format_research_result(result)
        
        current_research['status'] = 'completed'
        current_research['end_time'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'result': formatted_result,
            'research_info': current_research
        })
        
    except Exception as e:
        current_research['status'] = 'error' if current_research else None
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/pdfs')
def get_pdfs():
    """Get available PDFs"""
    global workflow
    
    if not workflow:
        return jsonify({
            'error': 'Workflow not initialized',
            'success': False
        }), 500
    
    try:
        pdf_notetaker = workflow.pdf_notetaker
        available_pdfs = pdf_notetaker.get_available_pdfs_for_selection()
        
        return jsonify({
            'success': True,
            'pdfs': available_pdfs
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/relevant-pdfs', methods=['POST'])
def get_relevant_pdfs():
    """Get PDFs ranked by relevance to query"""
    global workflow
    
    if not workflow:
        return jsonify({
            'error': 'Workflow not initialized',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query is required',
                'success': False
            }), 400
        
        pdf_notetaker = workflow.pdf_notetaker
        ranked_pdfs = pdf_notetaker.filter_and_rank_pdfs(query, max_pdfs=10)
        
        return jsonify({
            'success': True,
            'pdfs': ranked_pdfs
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/status')
def get_status():
    """Get current research status"""
    global current_research
    
    return jsonify({
        'success': True,
        'research': current_research,
        'workflow_ready': workflow is not None
    })

def format_research_result(result):
    """Format research result for web display"""
    try:
        research_type = getattr(result, "research_type", "general")
        
        formatted = {
            'research_type': research_type,
            'query': getattr(result, 'query', ''),
            'entities': [],
            'analysis': getattr(result, 'analysis', ''),
            'market_insights': None
        }
        
        # Format entities based on research type
        if hasattr(result, 'companies') and result.companies:
            # Developer tools format
            for company in result.companies[:5]:
                entity = {
                    'name': company.name,
                    'website': company.website,
                    'description': company.description,
                    'type': 'company',
                    'details': {
                        'pricing': company.pricing_model,
                        'open_source': company.is_open_source,
                        'tech_stack': company.tech_stack[:5] if company.tech_stack else [],
                        'api_available': company.api_available,
                        'languages': company.language_support[:5] if company.language_support else [],
                        'integrations': company.integration_capabilities[:4] if company.integration_capabilities else []
                    }
                }
                formatted['entities'].append(entity)
                
        elif hasattr(result, 'market_entities') and result.market_entities:
            # Market research format
            for entity in result.market_entities[:5]:
                formatted_entity = {
                    'name': entity.name,
                    'category': entity.category,
                    'website': entity.website,
                    'description': entity.description,
                    'type': entity.category,
                    'details': {}
                }
                
                # Add type-specific details
                if research_type == "product_research":
                    formatted_entity['details'] = {
                        'price': getattr(entity, 'price', 'Unknown'),
                        'rating': getattr(entity, 'rating', 'Unknown'),
                        'brand': getattr(entity, 'brand', 'Unknown'),
                        'features': getattr(entity, 'features', [])[:3],
                        'target_audience': getattr(entity, 'target_audience', 'Unknown')
                    }
                else:
                    # General details
                    formatted_entity['details'] = {
                        'market_position': getattr(entity, 'market_position', 'Unknown'),
                        'revenue': getattr(entity, 'revenue', 'Unknown'),
                        'employees': getattr(entity, 'employees', 'Unknown')
                    }
                
                formatted['entities'].append(formatted_entity)
        
        # Add market insights if available
        if hasattr(result, 'market_insights') and result.market_insights:
            insights = result.market_insights
            formatted['market_insights'] = {
                'market_size': insights.market_size,
                'growth_rate': insights.growth_rate,
                'key_drivers': insights.key_drivers,
                'market_trends': insights.market_trends
            }
        
        return formatted
        
    except Exception as e:
        print(f"Error formatting result: {e}")
        return {
            'research_type': 'error',
            'entities': [],
            'analysis': f'Error formatting results: {str(e)}',
            'market_insights': None
        }

if __name__ == '__main__':
    print("🚀 Starting Multi Agent Researcher Web UI...")
    
    # Initialize workflow
    init_workflow()
    
    if workflow:
        print("✅ Ready to serve requests!")
        app.run(debug=True, host='0.0.0.0', port=5002)
    else:
        print("❌ Failed to initialize. Please check your configuration.")