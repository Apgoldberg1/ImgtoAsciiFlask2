from flask import *  
import ImageAnalysis

app = Flask(__name__) 
app.secret_key = "wewraefsdaf"
@app.route('/', methods=['GET', 'POST'])  
def upload():
    if request.method == 'GET':
        session['file'] = ''  
        return render_template("file_upload_form.html")
    if request.method == 'POST':
        if 'file' in request.files: 
            f = request.files['file']  
            f.save("static/images/" + f.filename)
            session['file'] = f.filename
            dims = ImageAnalysis.process("static/images/" + f.filename)
            session['dims'] = dims
            session['edgeDetect'] = 3
            return render_template("success.html", name = session['file'], dims = dims, color = 'False', edgeDetect = session['edgeDetect'], invert='False', brightness=-100, contrast=1)

@app.route('/success', methods = ['GET', 'POST'])  
def success():
    if request.method == 'POST':
        color = 'True' if request.form.get('color') != None else 'False'
        invert = 'True' if request.form.get('invert') != None else 'False'

        brightness = float(request.form.get('brightness')) if request.form.get('brightness') != None else -100
        contrast = float(request.form.get('contrast')) if request.form.get('contrast') != None else 1
        session['edgeDetect'] =  request.form.get('edgeDetect')
        if request.form.get('scale') != session['dims']:
                session['dims'] = ImageAnalysis.process("static/images/" + session['file'], scale_factor=int(request.form.get('scale')), color=color, edgeDetect = session['edgeDetect'], invert=invert, brightness=brightness,contrast=contrast)
        return render_template("success.html", name = session['file'], scale = int(request.form.get('scale')), dims = session['dims'], color=color, fontSize = request.form.get('fontSize'), edgeDetect = session['edgeDetect'], invert=invert, contrast=request.form.get('contrast'), brightness=request.form.get('brightness'))   
if __name__ == '__main__':  
    app.run(port = 5000, debug = True)  