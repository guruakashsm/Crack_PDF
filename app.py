import PyPDF2
import itertools

def open_pdf_with_password(pdf_path, password):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if the PDF is encrypted
            if pdf_reader.is_encrypted:
                # Try to decrypt the PDF with the provided password
                if pdf_reader.decrypt(password):
                    # Successfully decrypted the PDF
                    num_pages = len(pdf_reader.pages)
                    print(f'Correct password: {password}')
                    raise SystemExit
                    return True
                    # Access individual pages or perform other operations as needed
            else:
                print('The PDF is not encrypted. No password required.')
                return True
                
    except FileNotFoundError:
        print(f'Error: File "{pdf_path}" not found.')
    except Exception as e:
        print(f'Error: {e}')

    return False

# Example usage
pdf_file_path = 'guru.pdf'
characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_+-=[]\\;\',./\{\}|:"<>?'

# Generate all possible combinations
for length in range(1, 999):
    combinations = itertools.product(characters, repeat=length)
    for combo in combinations:
        password = ''.join(combo)
        print(f'Trying password: {password}')
        if open_pdf_with_password(pdf_file_path, password):
            break  # Exit the loop if the correct password is found

