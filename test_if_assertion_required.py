"""
some testing to check the value of assertions
"""

def stringfun(val:str) -> str:
    return val

def stringassertfun(val: str) -> str:
    assert isinstance(val,str)
    return val

def main():
    val = 1
    stringfun(val)

    stringassertfun(val)

