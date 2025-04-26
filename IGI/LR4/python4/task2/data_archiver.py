import zipfile
import os

class DataArchiver:
    @staticmethod
    def archive_file(file_path, archive_path):
        with zipfile.ZipFile(archive_path, 'w') as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
            info = zipf.getinfo(os.path.basename(file_path))
            print(f"Archived: {info.filename}, Size: {info.file_size}, Compressed: {info.compress_size}")
