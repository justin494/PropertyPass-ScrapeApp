@app.route('/view_login',methods=['GET'])
def view_login():
    return render_template('Home.html')