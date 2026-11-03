from langchain_core.tools import tool
import re
from typing import Union, List, Dict


@tool
def add_numbers(inputs: str) -> dict:
    """
    Adds numbers in input string
    """
    numbers = [float(num) for num in re.findall(r"-?\d+(?:\.\d+)?", inputs)]
    result = sum(numbers)
    return {"result": result}


@tool
def add_numbers_with_options(numbers: List[float],
                             absolute: bool = False) -> float:
    """
    Adds a list of numbers
    """
    if absolute:
        numbers = [abs(n) for n in numbers]
    return sum(numbers)


@tool
def sum_numbers_with_complex_output(inputs: str) -> Dict[str, Union[float,
                                                                    str]]:
    """
    Extracts and sums all integers and decimal numbers from input string
    """
    matches = re.findall(r'-?\d+(?:\.\d+)?', inputs)
    if not matches:
        return {"result": "No numbers found in input"}
    try:
        numbers = [float(num) for num in matches]
        total = sum(numbers)
        return {"result": total}
    except Exception:
        return {"result": "Error during summation"}


@tool
def subtract_numbers(inputs: str) -> dict:
    """
    Extracts number from string and subtracts each number
    after the first number
    """
    numbers = [float(num) for num in re.findall(r"-?\d+(?:\.\d+)?", inputs)]
    if not numbers:
        return {"result": 0}
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return {"result": result}


@tool
def multiply_numbers(inputs: str) -> dict:
    """Extracts numbers from a string and calculates their product."""
    numbers = [float(num) for num in re.findall(r"-?\d+(?:\.\d+)?", inputs)]

    if not numbers:
        return {"result": 1}

    result = 1
    for num in numbers:
        result *= num
    return {"result": result}


@tool
def divide_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and divides the first by each
    subsequent number.
    """
    numbers = [float(num) for num in re.findall(r"-?\d+(?:\.\d+)?", inputs)]

    if not numbers:
        return {"result": 0}

    if any(num == 0 for num in numbers[1:]):
        return {"result": "Cannot divide by zero."}

    result = numbers[0]
    for num in numbers[1:]:
        result /= num
    return {"result": result}

# To build tools manually without decorator:
# from langchain_core.tools import Tool
# add_tool = Tool(
#     name="AddTool",
#     func=add_numbers,
#     description="Adds a list of numbers and returns the result"
# )
