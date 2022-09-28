import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/create', methods=['POST'])
def create_movies():
    try:        
        _json = request.json
        _name = _json['name']
        _img = _json['img']
        _summary = _json['summary']	
        if _name and _img and _summary  and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO Movies_data(name, img, summary) VALUES(%s, %s, %s)"
            bindData = (_name, _img, _summary)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Movies added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()          
     
@app.route('/movies')
def movie():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT name, img, summary, address FROM Movies_data")
        MoviesRows = cursor.fetchall()
        respone = jsonify(MoviesRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/movies/<char:movies_name>')
def movie_details(movies_name):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT name, img, summary FROM Movies_data WHERE name =%s", movies_name);
        MoviesRow = cursor.fetchone()
        respone = jsonify(MoviesRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/update', methods=['PUT'])
def update_movies():
    try:
        _json = request.json
        _name = _json['name']
        _img = _json['img']
        _summary = _json['summary']
        if _name and _img and _summary  and request.method == 'PUT':			
            sqlQuery = "UPDATE Movies_data SET name=%s, img=%s, summary=%s WHERE img=%s"
            bindData = (_name, _img, _summary)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Movies updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/delete/', methods=['DELETE'])
def delete_movies(name):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM Movies_data WHERE name =%s", (name,))
		conn.commit()
		respone = jsonify('Movies deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()