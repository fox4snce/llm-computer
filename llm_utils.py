"""
llm_utils.py - 

Usage:
- Ensure your local OpenAI-like server is running on port 5001
- Import this module and use the provided functions for text and JSON responses
"""

import json
import requests
import traceback

def generate_response(system=None, user_message=None, max_tokens=8192, temperature=0.8):
    try:
        if system is None:
            system = "You are a helpful coding assistant."
        if user_message is None:
            user_message = "You are a wonderful blog post writer."

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_message}
        ]

        data = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        response = requests.post(
            "http://localhost:5001/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=data,
            stream=True
        )

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line.decode('utf-8').split('data: ')[1])
                    if 'choices' in json_response and len(json_response['choices']) > 0:
                        content = json_response['choices'][0]['delta'].get('content', '')
                        full_response += content
                except:
                    pass

        return full_response
    except Exception as e:
        error_message = f"Error generating response: {str(e)}\n"
        error_message += f"System prompt: {system}\n"
        error_message += f"User message: {user_message}\n"
        error_message += f"Traceback:\n{traceback.format_exc()}"
        print(error_message)
        raise RuntimeError(error_message)

