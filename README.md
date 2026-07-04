<img width="1000" height="500" alt="Image" src="./img/gameplay.gif" />

# Blink Controller

A real-time eye blink controller built with **Python**, **MediaPipe**, **OpenCV**, and **CVZone**.

This project allows players to use space using eye blinks captured by a webcam. Instead of pressing a physical key, the system detects when the player's eye closes and automatically triggers the **Space** key.

---

## Features

- Real-time eye tracking
- Blink detection using Eye Aspect Ratio (EAR)
- Automatic Space key press and release
- Face landmark tracking using MediaPipe
- BlendShape facial analysis
- LivePlot visualization
- Webcam-based interaction

---

## How It Works

The system continuously captures frames from a webcam and processes them using MediaPipe Face Mesh.

MediaPipe generates a facial model containing up to **468 facial landmarks**. For blink detection, only the landmarks around the eye region are used.

The project calculates the **Eye Aspect Ratio (EAR)**, which measures the distance between eyelid landmarks.

### Eye Open

```text
Eye Open
→ Space Released
```

### Eye Closed

```text
Eye Closed
→ Space Pressed
```

The result is a simple control mechanism:

```text
Close Eye  → Jump
Open Eye   → Stop Jump
```

---

## Detection Method

The blink detection is based on the **Eye Aspect Ratio (EAR)**.

EAR is calculated using specific landmarks around the eye and provides a reliable measurement of whether the eye is open or closed.

The project also uses MediaPipe's **BlendShape model**, which provides additional facial analysis and improves the robustness of the detection process.

## Requirements

Before running the project, install:

### Python 3.11

Download Python from:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

or

```bash
py --version
```

---

## Installation

Clone the repository:

```bash
git clone git@github.com:Matheus-Sounier/Eye-Control-Gaming-System.git
```

Enter the project directory:

```bash
cd Eye-Control-Gaming-System
```

Create a virtual environment:

```bash
python -m venv venv
```

or specify Python 3.11:

```bash
py -3.11 -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run the main script:

```bash
python .\src\blink.py
```

If everything is configured correctly, the webcam window will open and blink detection will start automatically.

---

## Live Plot

The project includes a LivePlot graph that displays blink activity in real time.

The graph helps visualize:

- Eye opening
- Eye closing
- EAR value changes
- Detection threshold behavior

The Y-axis represents the eye openness level measured by the system.
