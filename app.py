from flask import Flask, render_template, request, redirect, url_for
import PyPDF2
import itertools
import concurrent.futures
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def open_pdf_with_password(pdf_path, password):
    try:
        print("Trying Password :",password)
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if pdf_reader.is_encrypted:
               
                if pdf_reader.decrypt(password):
                    num_pages = len(pdf_reader.pages)
                    return f'Correct password: {password}'
            else:
                return 'The PDF is not encrypted. No password required.'
                
    except FileNotFoundError:
        return f'Error: File "{pdf_path}" not found.'
    except Exception as e:
        return f'Error: {e}'
    
    return None

def password_cracker(pdf_file_path, characters, length):
    combinations = itertools.product(characters, repeat=length)
    for combo in combinations:
        password = ''.join(combo)
        result = open_pdf_with_password(pdf_file_path, password)
        if result:
            return result
    return None

def build_character_set(use_lower, use_upper, use_digits, use_special):
    characters = ''
    if use_lower:
        characters += 'abcdefghijklmnopqrstuvwxyz'
    if use_upper:
        characters += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if use_digits:
        characters += '0123456789'
    if use_special:
        characters += '~`!@#$%^&*()_+-=[]\\;\',./{}|:"<>?'
    return characters

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save the uploaded file
        pdf_file = request.files['pdf_file']
        if pdf_file:
            pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_file_path)
        
            # Get the user input from the form
            use_lower = 'use_lower' in request.form
            use_upper = 'use_upper' in request.form
            use_digits = 'use_digits' in request.form
            use_special = 'use_special' in request.form
            length_from = int(request.form['length_from'])
            length_to = int(request.form['length_to'])
            
            # Build the character set
            characters = build_character_set(use_lower, use_upper, use_digits, use_special)
            
            # Start the password cracking process
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for length in range(length_from, length_to + 1):
                    futures.append(executor.submit(password_cracker, pdf_file_path, characters, length))
                
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:  # If a correct password is found
                        return f'<h2>Password found: {result}</h2>'
            
            return '<h2>No valid password found in the given range.</h2>'
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
