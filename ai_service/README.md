# AI Answer Generation Service

AI service that generates answers to student questions using OpenAI's API with personalized context.

## Overview

This service provides intelligent answer generation by:
- Connecting to an OpenAI-compatible API
- Using conversation context for personalized responses
- Building educational prompts optimized for teaching

## Configuration

The service is configured to connect to:
- **OpenAI API Base URL**: `http://aiforge.cs.purdue.edu:8001/v1`
- **API Key**: `aiforge-65H3xnZtz757QJUJnGTARKaHmgb8_iMFAmS4T5VJup8`
- **Model**: `gpt-oss:120b`
- **Port**: `8901`

## API Endpoints

### POST /generate

Generate an AI answer for a question with optional context.

**Request:**
```json
{
  "question": "How do I implement backpropagation?",
  "context": [
    {
      "q": "What is a neural network?",
      "a": "A neural network is a computational model..."
    },
    {
      "q": "What is gradient descent?",
      "a": "Gradient descent is an optimization algorithm..."
    }
  ]
}
```

**Response:**
```json
{
  "answer": "Backpropagation is implemented by calculating gradients..."
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-generator"
}
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Service

```bash
# Development mode
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8901
```

## How It Works

1. **Context Integration**: The three previous Q&A pairs from the same student are included in the prompt to provide personalized, contextually-aware answers. This ensures that the AI model is able to give accurate proposed responses, as we expect students to have back-and-forth conversations in the same chat.

2. **Class Document Retrieval**: Past documents from the course pertaining to the student are also retrieved and injected into the prompt via a custom retrieval augmented generation system. These documents serve to give the AI model better technical context, thus resulting in a better answer content-wise

3. **Prompt Engineering**: The service builds educational prompts that encourage clear, concise explanations suitable for learning. This feature ensures that students don't abuse the platform for answers to assignments, but instead enriches their knowledge of the course's content

4. **Error Handling**: Robust error handling for API timeouts, connection issues, and malformed responses

## Testing

Test the service with curl:

```bash
# Simple question without context
curl -X POST http://localhost:8901/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "context": []
  }'

# Question with context
curl -X POST http://localhost:8901/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do neural networks learn?",
    "context": [
      {"q": "What is a neural network?", "a": "A computational model..."}
    ]
  }'
```

## Configuration Options

Edit the constants in `main.py`:

```python
OPENAI_BASE_URL = "http://aiforge.cs.purdue.edu:8001/v1"  # OpenAI API endpoint
OPENAI_API_KEY = "aiforge-65H3xnZtz757QJUJnGTARKaHmgb8_iMFAmS4T5VJup8"                         # API key
MODEL_NAME = "gpt-oss:120b"              # Model to use
REQUEST_TIMEOUT = 120.0                         # Request timeout in seconds
```

**Timeout Guidelines:**
- Small models (<7B): 30-60 seconds
- Medium models (7B-30B): 60-120 seconds
- Large models (30B-120B): 120-180 seconds
- Very large models (120B+): 180-300+ seconds

## Error Responses

The service gracefully handles errors and returns user-friendly messages:

- **Timeout**: "Request timed out. Please try again."
- **Connection Error**: "Unable to connect to AI service. Please try again later."
- **API Error**: "Unable to generate answer due to API error."
- **Unknown Error**: "An unexpected error occurred while generating the answer."

## Integration

This service is designed to work with the Q&A system's instructor panel, where it provides AI-generated answer suggestions that instructors can review and edit before sending to students.
