#!/usr/bin/env python3
import requests
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load face tokens from JSON file
try:
    with open('face_tokens.json', 'r') as f:
        data = json.load(f)
        faces = data["faces"]
except FileNotFoundError:
    print("Error: face_tokens.json file not found")
    exit(1)

compare_url = "https://api-us.faceplusplus.com/facepp/v3/compare"
face_tokens = [face["face_token"] for face in faces]

# API credentials from environment variables
API_KEY = os.getenv('FACEPP_API_KEY')
API_SECRET = os.getenv('FACEPP_API_SECRET')

if not API_KEY or not API_SECRET:
    print("Error: API credentials not found in .env file")
    exit(1)

# Check if results file exists
results_file = 'face_comparison_results.json'
if Path(results_file).exists():
    print("Loading existing comparison results...")
    with open(results_file, 'r') as f:
        comparison_results = json.load(f)
else:
    print("Performing new comparisons...")
    comparison_results = {
        'timestamp': datetime.now().isoformat(),
        'comparisons': []
    }
    
    for i in range(len(face_tokens)):
        for j in range(i+1, len(face_tokens)):
            data = {
                "api_key": API_KEY,
                "api_secret": API_SECRET,
                "face_token1": face_tokens[i],
                "face_token2": face_tokens[j]
            }
            try:
                response = requests.post(compare_url, data=data)
                response.raise_for_status()
                result = response.json()
                comparison = {
                    'face1': {'number': i+1, 'token': face_tokens[i]},
                    'face2': {'number': j+1, 'token': face_tokens[j]},
                    'confidence': result['confidence']
                }
                comparison_results['comparisons'].append(comparison)
            except requests.exceptions.RequestException as e:
                print(f"Error comparing faces: {e}")
    
    # Save results to file
    with open(results_file, 'w') as f:
        json.dump(comparison_results, f, indent=2)

# Print reference and results
print("\nFace Reference:")
for idx, token in enumerate(face_tokens):
    print(f"Face {idx+1}: {token}")

print("\nComparison Results:")
for comparison in comparison_results['comparisons']:
    face1 = comparison['face1']
    face2 = comparison['face2']
    confidence = comparison['confidence']
    print(f"Face {face1['number']} ({face1['token']}) and Face {face2['number']} ({face2['token']}): {confidence}% similar")
    if confidence > 80:
        print(f"⚠️  High similarity detected!")




