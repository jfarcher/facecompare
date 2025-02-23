# Face Comparison Tool

A Python application that uses Face++ API to detect and compare faces in images, with an interactive visualization tool.

![Original Image](IMG_0020.JPG)
*Original historical photograph*

![Application Interface](output.png)
*Interactive interface showing face comparisons*

## Overview

This tool analyses photographs to:
1. Detect faces in the image
2. Generate face tokens using Face++ API
3. Compare all faces with each other to find similarities
4. Provide an interactive interface to explore face relationships

## Features

- Face detection and token generation
- Automated face comparison using Face++ API
- Interactive visualization:
  - Click on any face to see its relationships
  - Color-coded similarity indicators
  - Percentage-based similarity scores
  - Green labels for easy identification

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- Requests
- python-dotenv
- [Face++ API account](https://www.faceplusplus.com/)

## Installation

1. Clone the repository
2. Create a virtual environment: