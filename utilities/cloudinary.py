import cloudinary.uploader
import config.cloudinary

def upload_image(file, folder: str = "recipes") -> dict:
    """
    Uploads a file to Cloudinary.
    
    :param file: The file to upload (can be a file path, file-like object, or bytes).
    :param folder: The folder name in Cloudinary where the file should be stored.
    :return: A dictionary containing the upload response (including 'secure_url' and 'public_id').
    """
    try:
        response = cloudinary.uploader.upload(file, folder=folder)
        return response
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
