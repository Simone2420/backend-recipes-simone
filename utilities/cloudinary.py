import cloudinary.uploader
import config.cloudinary

def upload_image(file, folder: str = "recipes") -> str:
    """
    Uploads a file to Cloudinary.
    
    :param file: The file to upload (can be a file path, UploadFile, file-like object, or bytes).
    :param folder: The folder name in Cloudinary where the file should be stored.
    :return: The secure URL string of the uploaded image.
    """
    try:
        # Si es un objeto UploadFile de FastAPI/Starlette, extraemos el archivo subyacente
        file_to_upload = getattr(file, "file", file)
        response = cloudinary.uploader.upload(file_to_upload, folder=folder)
        return response.get("secure_url")
    except Exception as e:
        raise e

def delete_image(public_id: str) -> dict:
    """
    Deletes an image from Cloudinary using its public ID.
    
    :param public_id: The public ID of the image to delete.
    :return: A dictionary containing the deletion response.
    """
    try:
        response = cloudinary.uploader.destroy(public_id)
        return response
    except Exception as e:
        raise e
