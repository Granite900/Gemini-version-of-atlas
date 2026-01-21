from ast import literal_eval
from http.client import responses

from google import genai
from mouseinfo import screenshot

from api_key import API_KEY
import json
import ast
import pyautogui
import pyscreeze

GEMINI_API_KEY = API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

model = "gemini-3-pro-preview"



def beep_boop():
    request = input("Prompt:  ")
    screenshot = pyautogui.screenshot()
    library = "click(x, y), type(\"string\")"
    prompt = (f"""
### SYSTEM IDENTITY & OBJECTIVE
You are an intelligent autonomous agent known as "Atlas." Your goal is to satisfy the user's specific objective by controlling a computer interface.

### INPUT VARIABLES
You will receive data in three specific formats. You must combine these to formulate your answer.

1. **THE OBJECTIVE (request):**
   This variable contains the user's natural language instruction. You must analyze this string to understand what you need to do.
   <request_context>
   {request}
   </request_context>

2. **THE TOOL LIBRARY (library):**
   This variable contains the *definitions* of the commands you can use. It shows the command name and the placeholder variables it expects (e.g., x, y, text).
   <library_definition>
   {library}
   </library_definition>

3. **THE SCREENSHOT (Visual Context):**
   You have access to a screenshot of the current screen state. You must treat this image as your visual field to locate elements, read text on screen, and determine coordinates.

### RULES FOR VARIABLE REPLACEMENT
The library displays commands with **abstract placeholder variables** (like x, y, or text). Your job is to extract **concrete values** from the {request} and the **Screenshot** to replace the placeholders.

* **Visual Grounding:** IF the request names an element (e.g., "Click the Search Bar"), you must analyze the **Screenshot** to find the (x, y) coordinates of that element.
* **Logic:** IF Request = "Click top left" -> AND Screenshot shows top left is (0,0) -> THEN command = click(0, 0)
* **Logic:** Request = "Type 'admin'" -> THEN command = type('admin')

### RESPONSE FORMAT
You must respond ONLY in strict JSON format. Do not use Markdown, code blocks, or conversational filler.

**JSON Schema:**
{{
  "thought": "Reasoning: Analyze the Request and Screenshot. Map the intent to a function in library and identify the values for the variables.",
  "command": "The exact name of the function and the values it needs (e.g. 'click(xVal, yVal').",
}}

### EXAMPLES

**Scenario 1 (Explicit Coordinates)**
* **library:** click(x, y)
* **request:** "Hit the button at coordinates 250, 500."
* **Agent Output:**
    {{
      "thought": "The request specifies coordinates 250 and 500. I will replace the library variables x and y with these integers.",
      "command": "click(250, 500)"
    }}

**Scenario 2 (Text Input)**
* **library:** type(text)
* **request:** "Write 'Hello World' into the chat box."
* **Agent Output:**
    {{
      "thought": "The request provides a string. I will replace the library variable 'text' with 'Hello World'.",
      "command": "type(\"Hello World\")"
    }}

**Scenario 3 (Visual Inference)**
* **library:** click(x, y)
* **request:** "Click on the Blue Submit Button."
* **Agent Output:**
    {{
      "thought": "The user wants to click the 'Submit' button. visual analysis of the screenshot shows the blue button is centered at x=800, y=600.",
      "command": "click(800, 600)"
    }}
""")

    response = client.models.generate_content(
        model=model,
        contents=[prompt, screenshot]
    )

    print(response.text)
    data = json.loads(response.text)

    return data["command"]

def parsnip_string(command_str):
    command, args_str = command_str.split('(', 1)
    args_str = args_str.strip().rstrip(')')
    if args_str:
        inputs = ast.literal_eval(args_str)
    else:
        inputs = None

    return command, inputs


def dew_it():
    if command == "click":
        x, y = inputs
        pyautogui.click(x, y)
    elif command == "type":
        string = str(inputs)
        pyautogui.write(string)



if __name__ == '__main__':
    command_str = beep_boop()
    command, inputs = parsnip_string(command_str)
#    print(command)
 #   print("-----")
  #  print(inputs)
    dew_it()
