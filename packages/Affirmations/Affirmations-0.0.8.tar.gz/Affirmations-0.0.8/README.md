# Affirmations

A module that gives you a little bump of encouragement. 

## Requirements
- A positive attitude
- A can-do spirit

## Installation

```bash
pip install Affirmations
```

## Usage

Decorate any function to get a random affirmation printed to stdout every time that function is run

```
from Affirmations import affirm

@affirm
def hello_world():
    print("hello")

hello_world()
```
```bash
hello
You are awesome!
```