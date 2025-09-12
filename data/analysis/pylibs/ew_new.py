from openpyxl import load_workbook
from PIL import Image
import io

def extract_image_at_cell(xlsx_path, sheet_name, target_cell, save_path=None):
    """
    Extracts the image anchored to a specific cell in an Excel sheet.

    Parameters:
        xlsx_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to inspect.
        target_cell (str): Cell reference (e.g., 'B2') where the image is anchored.
        save_path (str, optional): If provided, saves the image to this path.

    Returns:
        PIL.Image.Image: The extracted image object, or None if not found.
    """
    wb = load_workbook(xlsx_path)
    ws = wb[sheet_name]

    for img in getattr(ws, "_images", []):
        anchor = getattr(img.anchor, "_from", None)
        if anchor:
            col_letter = chr(65 + anchor.col)
            row_number = anchor.row + 1
            anchored_cell = f"{col_letter}{row_number}"
            if anchored_cell == target_cell:
                image_data = img._data()
                image = Image.open(io.BytesIO(image_data))
                if save_path:
                    image.save(save_path)
                return image

    return None