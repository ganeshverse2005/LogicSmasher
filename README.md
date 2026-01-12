Logic Smasher Visualizer "Understand any logic."

Code Smasher is a tool designed to break down Python source code into an interactive flow graphs.
It uses LLMs (Groq + Llama 3) to analyze your scripts and visualizes the execution flow using Cytoscape.js.

Capabilities

LLM-Based Analysis: Uses LangChain and Groq (Llama-3-70b/8B) to map relationships, distinguishing between internal functions and external library calls.

Deep Inspection: Click any node to see input parameters, return types, and context (Global vs Class Method).

Auto-Formatting: Automatically formats pasted code with Black before analysis.

Dynamic UI: Features a resizeable workspace and a physics-based particle animation on entry.

Tech Stack

Frontend: HTML5/CSS, JavaScript, Cytoscape.js

Backend: Python 3, Flask, LangChain, Groq API, Black

Roadmap:
I am currently using LLMs for rapid parsing flexibility, but the project is evolving toward high-performance static analysis.

Transition to Pure AST: Moving to Python's native ast module for zero latency and no API rate limits.

Documentation Generator: Auto-generating docstrings for every node.

Multi-File Support: Support for uploading entire folders.

Language Agnostic: Expanding support to JavaScript, C++, and Rust.
