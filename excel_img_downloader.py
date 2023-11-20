import pandas as pd
import requests
from pathlib import Path
import concurrent.futures
from urllib.parse import urlparse
import winsound

def get_image_name(url):
    # Extract the image name from the URL
    path = urlparse(url).path
    return Path(path).stem

def download_image(i, url):
    try:
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                # Get the image name from the URL
                image_name = get_image_name(url)
                with open(Path('C://Users//raaj//Desktop//fatafeat menu//imageUrls4') / f'{image_name}.jpg', 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {image_name}.jpg")
            else:
                print(f"Failed to download image {url}. Status code: {response.status_code}")
        else:
            print(f"Skipping row {i} as it does not have a valid URL")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {str(e)}")

xl = pd.ExcelFile('C://Users//raaj//Desktop//fatafeat menu.xlsx')  # Filepath
df = xl.parse('With Multiple Images')  # SheetName

start_index = 0  # Starting row index for downloading images
end_index = 3860  # Ending row index for downloading images

# Create a ThreadPoolExecutor for concurrent downloading
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Download images in parallel, but only if the URL is not empty or None
    futures = {executor.submit(download_image, i, url) for i, url in enumerate(df['imageUrls4'][start_index:end_index + 1]) if url}
    concurrent.futures.wait(futures)

# Play a beep sound to indicate completion
winsound.Beep(1000, 500)  # You can adjust the frequency (1000) and duration (500) as needed
