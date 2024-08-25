from enum import auto
from logging import raiseExceptions
from flask import Flask, request, Response, make_response
import uuid

app = Flask(__name__)
calculator = {}
auto_id = 0

def valid_request(request):
    if request.method == "POST":
        body = request.get_json()
        if "value" in body:
            return True
        else:
            return False
    else:
        raise Exception("Invalid method")
        # return "Invalid method", 405
    
def get_id(body):
    global auto_id  
    if "id" in body:
        id = body.get("id")
        if id not in calculator:
            raise Exception("Id not found")
    else:
        id = auto_id
        calculator[id] = [0]
        auto_id += 1
    return id

@app.route("/add", methods=['POST'])
def get_addition():
    if valid_request(request):
        body = request.get_json()
        value = body.get("value")
        id = get_id(body)
    else:
        return "Invalid request", 400
    print(value)
    calculator[id].append(calculator[id][-1]+value)
    return {"id":id, "operation":"addition"}, 200

@app.route("/subtract", methods=['POST'])
def get_difference():
    if valid_request(request):
        body = request.get_json()
        value = body.get("value")
        id = get_id(body)
    else:
        return "Invalid request", 400
    calculator[id].append(calculator[id][-1]-value)
    return {"id":id, "operation":"subtraction"}, 200

@app.route("/multiply", methods=['POST'])
def get_product():
    if valid_request(request):
        body = request.get_json()
        value = body.get("value")
        id = get_id(body)
    else:
        return "Invalid request", 400
    calculator[id].append(calculator[id][-1]*value)
    return {"id":id, "operation":"multiplication"}, 200

@app.route("/divide", methods=['POST'])
def get_division():
    if valid_request(request):
        body = request.get_json()
        value = body.get("value")
        id = get_id(body)
    else:
        return "Invalid request", 400
    try:
        calculator[id].append(calculator[id][-1]/value)
    except ZeroDivisionError:
        return "Cannot divide by zero", 400
    return {"id":id, "operation":"division"}, 200



@app.route("/ans/<int:id>", methods=['GET'])
def get_ans(id):
    if request.method == "GET":
        if id not in calculator:
            return "Id not found", 404
        return str(calculator[id][-1]), 200
    else:
        return "Invalid method", 405
    
@app.route("/")
def home():
    return "Server is running\n"
      


if __name__ == "__main__":
    app.run(debug=True)

    #calculator is dictionary of differnet calculations
    #each post request gets me a unique value
    #get request for the total answer