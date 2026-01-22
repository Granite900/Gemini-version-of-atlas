from ast import literal_eval
from http.client import responses
from google import genai
from mouseinfo import screenshot
from api_key import API_KEY
import json
import ast
import pyautogui
from types import SimpleNamespace
import pyscreeze
from time import sleep

GEMINI_API_KEY = API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

model = "gemini-3-flash-preview"

screen_w, screen_h = pyautogui.size()
resolution = f"{screen_w}x{screen_h}"

def beep_boop():
    request = input("Prompt:  ")
    screenshot = pyautogui.screenshot()
    library = "click(x, y), type(\"string\"), press(\"key\")"
    prompt = (f"""
### SYSTEM IDENTITY & OBJECTIVE
You are "Atlas," a precision-focused autonomous agent. Your goal is to control a computer interface by analyzing visual inputs and executing actions.

### INPUT VARIABLES
1. **THE OBJECTIVE (request):**
   User's instruction:
   <request_context>
   {request}
   </request_context>

2. **THE TOOL LIBRARY (library):**
   Available commands:
   <library_definition>
   {library}
   </library_definition>

3. **THE SCREENSHOT (Visual Context):**
   You have access to a screenshot.
   **Screen Resolution:** {resolution}

### CRITICAL RULES FOR COORDINATE ACCURACY
You must strictly follow these rules to calibrate your aim:

1. **Y-AXIS CORRECTION (The +60 Offset):**
   * **Calibration:** Previous attempts were clicking "too high" by 120px when using a negative offset.
   * **Correction:** You must **ADD 60 PIXELS** to the calculated center to shift the aim down.
   * **Formula:** Target Y = (Top_Edge + Height * 0.50) + 60.
   * **Visual Aim:** Locate the geometric center, then shift your target DOWN by 60 pixels.

2. **Label vs. Container:**
   * IF the user says "Click Email," find the text "Email," but click the **input box** next to/below it.
   * Do NOT click the text. Click the container.

3. **Coordinate Grid:**
   * Map the image to a grid. (0,0) is TOP-Left.
   * **Important:** Increasing Y moves the click DOWN.

### RESPONSE FORMAT
Respond ONLY in a strict JSON **List (Array)**.

**JSON Schema:**
[
  {{
    "thought": "Analysis: Element found at [box coords]. Center Y is [y]. Applying +60px offset. Target: [x, y].",
    "command": "function(args)"
  }}
]

### EXAMPLES

**Scenario 1 (Button Click)**
* **library:** click(x, y), type(text)
* **resolution:** 1920x1080
* **request:** "Click the 'Submit' button."
* **Agent Output:**
    [
      {{
        "thought": "I found the 'Submit' button. Bounding box Top:600, Bottom:650 (Height=50). Center Y is 625. Applying +60px offset. Target Y = 685.",
        "command": "click(960, 685)"
      }}
    ]

**Scenario 2 (Form Entry)**
* **library:** click(x, y), type(text)
* **resolution:** 1920x1080
* **request:** "Type 'Hello' in the Chat."
* **Agent Output:**
    [
      {{
        "thought": "Found chat input. Box Top:900, Height 50. Center Y is 925. +60px offset => 985.",
        "command": "click(950, 985)"
      }},
      {{
        "thought": "Field focused. Typing text.",
        "command": "type(\"Hello\")"
      }}
    ]
**Scenario 3 (Form Entry)**
* **library:** click(x, y), type(text)
* **resolution:** 1920x1080
* **request:** "Google how to make cookies."
* **Agent Output:**
    [
        {{
            "thought": "Found search input. Box Top:900, Height 50. Center Y is 925. +60px offset => 985.",
            "command": "click(960, 453)"
        }},
        {{
            "thought": "Field focused. Typing text.",
            "command": "type(\"How to make cookies.\")"
        }}
        {{
            "thought": "Pressing enter to search"
            "command": "press(\"enter\")"
        }}
    ]
""")

    response = client.models.generate_content(
        model=model,
        contents=[prompt, screenshot]
    )

    print(response.text)

    return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))


def parsnip_string(command_str):
    command, args_str = command_str.split('(', 1)
    args_str = args_str.strip().rstrip(')')
    if args_str:
        inputs = ast.literal_eval(args_str)
    else:
        inputs = None

    return command, inputs


def dew_it():
    for step in commands:
        command, inputs = parsnip_string(step.command)
        if command == "click":
            x, y = inputs
            pyautogui.click(x, y)
        elif command == "type":
            string = str(inputs)
            pyautogui.write(string)
        elif command == "press":
            string = str(inputs)
            pyautogui.press(string)



if __name__ == '__main__':
    commands = beep_boop()
    dew_it()
