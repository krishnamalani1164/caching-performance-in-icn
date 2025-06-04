import os

def rename_and_cleanup_images(folder_path, animal_name):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter for only .jpg and .JPG files
    jpg_files = [f for f in files if f.lower().endswith('.jpg')]

    # Debugging: Print the total number of jpg files found
    print(f"Found {len(jpg_files)} .jpg files in the {animal_name} folder.")

    # Rename only the first 50 .jpg files to cat_image1.jpg, cat_image2.jpg, ..., or dog_image1.jpg, dog_image2.jpg, etc.
    for index, file_name in enumerate(jpg_files[:50], start=1):  # Limit to the first 50 files
        new_name = f"{animal_name}_image{index}.jpg"
        old_file = os.path.join(folder_path, file_name)
        new_file = os.path.join(folder_path, new_name)

        # Debugging: Print before renaming
        print(f"Renaming {old_file} to {new_file}")

        try:
            os.rename(old_file, new_file)
        except Exception as e:
            print(f"Error renaming {old_file}: {e}")

    # Delete the rest of the files (after the first 50)
    for file_name in jpg_files[50:]:
        file_to_delete = os.path.join(folder_path, file_name)

        # Debugging: Print before deleting
        print(f"Deleting {file_to_delete}")

        try:
            os.remove(file_to_delete)
        except Exception as e:
            print(f"Error deleting {file_to_delete}: {e}")

# Prompt user to input the paths for the cat and dog folders
cat_folder = input("Enter the full path of the cat images folder: ")
dog_folder = input("Enter the full path of the dog images folder: ")

# Rename and clean up both cats and dogs folders
rename_and_cleanup_images(cat_folder, "cat")
rename_and_cleanup_images(dog_folder, "dog")
