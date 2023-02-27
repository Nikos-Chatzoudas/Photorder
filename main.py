import os
from PIL import Image

# Function to extract the date from the metadata of a photo
def get_date_taken(path):
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()
            if exif_data:
                date_taken = exif_data.get(36867)
                return date_taken
    except:
        return None

# Function to move a file to a folder based on the year it was taken
def move_file(path, year):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(year):
        os.mkdir(year)

    # Build the destination path
    dest_path = os.path.join(year, os.path.basename(path))

    # Move the file
    os.rename(path, dest_path)
    print(f"{path} moved to {dest_path}")

# Check if the 'pdump' folder exists
if not os.path.exists("pdump"):
    raise Exception("pdump folder not found")

# Iterate over the files in the 'pdump' folder
for filename in os.listdir("pdump"):
    # Build the full path of the file
    filepath = os.path.join("pdump", filename)

    # Check if the file is a photo or video
    if filepath.endswith(("jpg", "jpeg", "png", "mp4","mkv")):
        # Extract the date the photo/video was taken from the metadata
        date_taken = get_date_taken(filepath)
        if date_taken:
            # Extract the year from the date
            year = date_taken.split(':')[0]
            # Move the file to the appropriate folder based on the year
            move_file(filepath, year)
        else:
            if not os.path.exists("Unknown year"):
                os.mkdir("Unknown year")
            move_file(filepath, "Unknown year")
    else:
        print(f"{filename} is not a supported file type")

input("Press Enter to exit")
