import json
from os import path
from urllib import response
from idna import valid_contextj
from requests import request
from app import app as myapp, calculator, valid_request, get_id
import pytest
from flask import request
import unittest
from mock import patch


# r = request("GET", "http://localhost:5000", headers={"Content-Type":"application/json"}, )

@pytest.fixture()
def app():
    app = myapp()
    app.config.update({"TESTING":True})

    return app

@pytest.fixture()
def client(app):
    return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()

def test_server_running():
    response = myapp.test_client().get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Server is running\n"

def test_calculator_empty():
    assert len(calculator) == 0

def test_addition_no_id():
    response = myapp.test_client().post("/add", json={"value":5})
    assert response.status_code == 200
    assert response.json == {"id":0, "operation":"addition"}

def test_ans():
    response = myapp.test_client().get("/ans/0")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "5"

def test_subtraction_no_id():
    response = myapp.test_client().post("/subtract", json={"value":5})
    assert response.status_code == 200
    assert response.json == {"id":1, "operation":"subtraction"}

    
def test_addition_id():
    response = myapp.test_client().post("/add", json={"value":5})
    assert response.status_code == 200
    assert response.json == {"id":2, "operation":"addition"}

    response = myapp.test_client().post("/add", json={"id":0,"value":5})
    assert response.status_code == 200
    assert response.json == {"id":0, "operation":"addition"}

def test_calculator():
    assert len(calculator) > 0


def test_zero_division():
    response = myapp.test_client().post("/divide", json={"value":0})
    assert response.status_code == 400
    assert response.data.decode("utf-8") == "Cannot divide by zero"


def test_valid_request():
    with myapp.test_request_context("/add", json = {"value":5000}, method="POST"):
        assert valid_request(request) == True

    with myapp.test_request_context("/add", json = {"vanhjhue":5000}, method="POST"):
        assert valid_request(request) == False

    with myapp.test_request_context("/add", json = {"value":5000}, method="GET"):
        with pytest.raises(Exception) as err:
            valid_request(request)
            assert str(err.value) == "Invalid method"
        
@patch("app.calculator", {5: 10, 7: 12})
@patch("app.auto_id", 6)
def test_get_id():
    body = {"id":5, "value":5000}
    body2 = {"value":5000}
    body3 = {"id":8, "value":7000}
    assert get_id(body) == 5

    assert get_id(body2) == 6

    with pytest.raises(Exception) as err:
        get_id(body3)
        assert str(err.value) == "Id not found"
