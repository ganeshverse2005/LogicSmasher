import os
import black
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional




app = Flask(__name__)
CORS(app)

class FunctionNode(BaseModel):
    id: str = Field(description="Unique identifier (e.g., func_name)")
    label: str = Field(description="Display name")
    type: str = Field(description="'function', 'method', 'external'")
    module: str = Field(description="The package/class it belongs to (e.g. 'numpy', 'Class User', 'Global')")
    params: str = Field(description="Input parameters")
    returns: str = Field(description="Return type/description")
    calls_count: int
    called_by_count: int

class CallEdge(BaseModel):
    source: str = Field(description="Caller ID")
    target: str = Field(description="Callee ID")
    order: int = Field(description="The sequential order of this call within the source function (1, 2, 3...)")

class CodeAnalysis(BaseModel):
    nodes: List[FunctionNode]
    edges: List[CallEdge]

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
parser = JsonOutputParser(pydantic_object=CodeAnalysis)

system_prompt = """
You are a Python Static Analysis Engine. 
Analyze the code to extract a Call Graph.

RULES:
1. Identify all internal functions and external library calls.
2. **Context:** For external calls, identify the package (e.g., 'json.load' -> module: 'json').
3. **Ordering:** For every function, track the order of calls inside it. If 'main' calls 'foo' then 'bar', the edge main->foo is order 1, main->bar is order 2.
4. Output strict JSON.
"""

human_prompt = "Analyze this code:\n{code}\n{format_instructions}"

prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
chain = prompt | llm | parser



@app.route('/format', methods=['POST'])
def format_code():
    """Auto-formats Python code using Black"""
    data = request.json
    code = data.get('code', '')
    try:
        formatted = black.format_str(code, mode=black.Mode())
        return jsonify({"code": formatted})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/smash', methods=['POST'])
def smash_code():
    data = request.json
    try:
        result = chain.invoke({
            "code": data.get('code', ''),
            "format_instructions": parser.get_format_instructions()
        })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    app.run(debug=True, port=5000)