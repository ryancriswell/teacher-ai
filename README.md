# Teacher AI - Worksheet Generator

A web application that generates customized educational worksheets for kindergarten teachers using AI. 

The system combines Large Language Models (LLMs) and image generation models to create fully personalizable materials to enhance student engagement and learning.

## Features

- **Word Bubble Worksheets**: Creates worksheets with images and letter bubbles to help students learn first letter sounds
- **Theme-Based Generation**: Generate worksheets based on specific themes (e.g., Thanksgiving, Animals, etc.)
- **AI-Generated Images**: Uses Stable Diffusion to generate child-friendly black and white coloring images
- **Customizable Layout**: 3x3 grid layout with clear letter choices below each image
- **PDF Output**: Generates professional-quality PDF worksheets with name fields and decorative borders
- **Extensibility**: Image generation structure is fully reusable with any additionally created templates.

## Technology Stack

- Python / Flask
- LangChain for LLM integration
- Stable Diffusion for image generation
- Pyngrok for tunneling
- ReportLab for PDF generation

## Getting Started

1. Clone the repository
2. Set up environment variables:
   ```
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

3. Start the backend:
   ```bash
   python server.py
   ```

## Usage

1. Open the frontend (https://github.com/ryancriswell/teacher-ai-ui)
2. Select "Word Bubbles" template
3. Enter a theme for the worksheet
4. Click "Generate PDF"
5. Download and print the generated worksheet

## Project Structure

```
teacher-ai/
│   ├── agent/        # LLM integration
│   ├── model/        # Data models
│   ├── worksheet/    # PDF generation and templates
│   └── server.py     # Flask server
```