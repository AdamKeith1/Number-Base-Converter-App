from flask import Flask, render_template, request

Flask_App = Flask(__name__) # Create Flask Instance

@Flask_App.route('/', methods=['GET'])
def index():
    '''Import HTML template'''

    return render_template('index.html')

@Flask_App.route('/operation_result/', methods=['POST'])
def operation_result():

    error = None
    result = None

    first_input = request.form['Input1'].lower()
    operation = request.form['operation']

    try:
        input1 = str(first_input) 

        # Default Binary -> Decimal
        if operation == "0b -> 0d":
            exp = len(input1) - 1 
            sum = 0
            for num in input1:
                sum += (int(num)*2) ** exp
                exp -= 1
            if input1[-1] == '0':
                sum -= 1
                
            result = sum

        elif operation == "0x -> 0d":
            hex_map = {
                'f': 15, 'e': 14, 'd': 13, 'c': 12, 'b': 11, 'a': 10
            }
            exp = len(input1) - 1
            sum = 0
            for num in input1:
                if num in hex_map:
                    sum += (hex_map[num]*16) ** exp
                else:
                    sum += (int(num)*16) ** exp
                exp -= 1
            
            if input1[-1] in hex_map:
                sum += hex_map[input1[-1]] - 1
            else:
                sum += num(input1[-1]) - 1
            
            result = sum

        elif operation == "0d -> 0b":
            num = int(input1)
            string = ''
            bin_string = DecimalToBinary(num, string)
            
            result = bin_string

        elif operation == "0d -> 0x":
            num = int(input1)
            result = hex(num)[2:]

        return render_template(
            'index.html',
            input1=input1,
            operation=operation,
            result=result,
            calculation_success=True
        )
        
    except ValueError:
        return render_template(
            'index.html',
            input1=first_input,
            operation=operation,
            result="Bad Input",
            calculation_success=False,
            error="Invalid format for given conversion"
        )
    
def DecimalToBinary(val, bin_string):
    if val >= 1:
        bin_string = DecimalToBinary(val // 2, bin_string) + str(val % 2)
    return bin_string

def DecimalToHex(val, hex_string):
    hex_map = {
                'f': 15, 'e': 14, 'd': 13, 'c': 12, 'b': 11, 'a': 10
            }
    if val >= 1:
        hex_string = DecimalToHex(val // 16, hex_string)

if __name__ == '__main__':
    Flask_App.debug = True
    Flask_App.run()
