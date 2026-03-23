# Wordy CV Solver

**OCR-based Computer Vision Pipeline for Solving Wordle-Style Word Puzzles**

---

## Overview

This project implements an **end-to-end computer vision and OCR pipeline** to solve Wordle-style puzzles **directly from images**.  
Instead of accessing game data programmatically, the system:

- Reads the game board visually  
- Extracts letters using OCR (Tesseract)  
- Tracks known letters and their positions  
- Generates optimal guesses for the next word  

---

## Modular Architecture
  - `vision/` → image processing & OCR
  - `solver/` → decision logic  
  - `game/` → simulation engine

---

## Tech Stack
  - Python 3
  - OpenCV
  - Pillow (PIL)
  - pytesseract
  - NumPy
