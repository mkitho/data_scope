from werkzeug.utils import secure_filename
from app import app 
from flask import render_template, request, redirect, url_for
from app.forms import UploadForm
from app.reporting import generate_statistics
import os

app.config['MAX_CONTENT_LENGTH'] = 1024 ** 3
app.config['UPLOAD_PATH'] = 'tmp'

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)
        # filename = 'tmpfile'
        if filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return redirect('/report/'+filename)
    return render_template("upload.html", form=form)

#### Use this chunk if not using flask-WTF form

# def upload():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         filename = secure_filename(uploaded_file.filename)
#         if filename != '':
#             uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#         return redirect('/report/'+filename)
#     else: 
#         return render_template("upload.html")

@app.route('/report/<filename>')
def report(filename):
    try:
        column_stats = generate_statistics(filename)
        os.remove(os.path.join(app.config['UPLOAD_PATH'], filename)) # removes user file
        return render_template("report.html", column_stats=column_stats, filename=filename)
    except:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], filename)) # removes user file
        message = "Sorry. There is an error processing your file"
        return render_template("upload.html", form=None, message=message)