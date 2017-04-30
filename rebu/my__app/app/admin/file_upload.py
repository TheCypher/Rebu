import os
from werkzeug.utils import secure_filename
import config

def file_upload(upload_file):
	if upload_file and allowed_file(upload_file.filename):
		filename = secure_filename(upload_file.filename)
		upload_file.save(os.path.join(config.UPLOAD_FOLDER, filename))
		return True

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.',1)[1].lower() in config.ALLOWED_EXTENSIONS
