def sum(input1, input2):
    if isinstance(input1,int) and isinstance(input2,int):
        sumNumber = input1 + input2
        return sumNumber
    else:
        return "please enter digit only."
    

def sub(input1, input2):
    if isinstance(input1,int) and isinstance(input2,int):
        subNumber = input1 - input2
        return subNumber
    else:
        return "please enter digit only."
    

def mul(input1, input2):
    if isinstance(input1,int) and isinstance(input2,int):
        mulNumber = input1 * input2
        return mulNumber
    else:
        return "please enter digit only."

def div(input1, input2):
    if isinstance(input1,int) and isinstance(input2,int):
        divNumber = input1 / input2
        return divNumber
    else:
        return "please enter digit only."
    
def divfl(input1, input2):
    if isinstance(input1,int) and isinstance(input2,int):
        divFloorNumber = input1 // input2
        return divFloorNumber
    else:
        return "please enter digit only."