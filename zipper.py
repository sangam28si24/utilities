import os
import pyzipper

def zip_and_encrypt_folder(folder_path, output_zip, password):
    # Create a zip file with AES encryption
    with pyzipper.AESZipFile(output_zip,
                             'w',
                             compression=pyzipper.ZIP_DEFLATED,
                             encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password.encode('utf-8'))
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Keep folder structure
                zipf.write(file_path, arcname)

    print(f"✅ Folder '{folder_path}' successfully zipped and encrypted as '{output_zip}'.")

# Example Usage
folder_to_zip = r"D:\Ehe"
output_file = r"D:\Ehe.zip"
password = "your_password_here"

zip_and_encrypt_folder(folder_to_zip, output_file, password)
