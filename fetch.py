import requests
from bs4 import BeautifulSoup
import os
import re
import yt_dlp

URL = "https://apod.nasa.gov/apod/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

def fetch_explanation():
    # Locate the "Explanation:" <b> tag, checking for different structures
    explanation_tag = soup.find(lambda tag: tag.name == "b" and "explanation" in tag.get_text().lower())

    if explanation_tag:
        # Try to find the paragraph containing the explanation text
        explanation_paragraph = explanation_tag.find_parent(["p", "center"])

        if explanation_paragraph:
            # Extract the text content of the explanation
            full_text = explanation_paragraph.get_text(" ", strip=True)

            # Use regex to extract the text after "Explanation:" up to "Tomorrow's picture" or similar indicators
            match = re.search(r"Explanation:\s*(.*?)(?=\s*(?:Tomorrow's picture|<center>|<b>|$))", full_text, re.S)

            if match:
                # Clean up the explanation text
                explanation_text = match.group(1).strip()
                explanation_text = re.sub(r'\s+\.$', '.', explanation_text).replace("\n", " ")
                return explanation_text
            else:
                print("Debug: Explanation regex match not found.")
                return "Explanation text not found."
        else:
            print("Debug: Explanation paragraph tag not found.")
            return "Explanation paragraph not found."
    else:
        print("Debug: Explanation tag not found.")
        return "Explanation tag not found."

def fetch_title_credit():
    # Find the title, which is in bold <b> tags after "Astronomy Picture of the Day"
    title_tag = soup.find("b")  # The first <b> tag contains the title
    title = title_tag.get_text(strip=True) if title_tag else "Title not found"

    # Find the image credit, which is the <a> tag after the title <b>
    image_credit_tag = title_tag.find_next_sibling("b").find_next("a")
    image_credit = image_credit_tag.get_text(strip=True) if image_credit_tag else "Image credit not found."

    # Find the copyright information, which is in the <a> tag that follows the copyright <b> tag
    copyright_tag = title_tag.find_next_sibling("b").find_next_sibling("a")
    copyright_info = copyright_tag.get_text(strip=True) if copyright_tag else "Copyright info not found."

    # Concatenate image credit and copyright info for a single string
    credit_info = f"Image Credit & Copyright: {copyright_info}"

    return title, credit_info

def fetch_img():
    image_tag = soup.find("img")
    if image_tag:
        image_url = "https://apod.nasa.gov/apod/" + image_tag['src']  # Complete the image URL
        print(f"Image URL: {image_url}")
        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Create a directory to save images if it doesn't exist
            os.makedirs("/media", exist_ok=True)
            image_name = "apod.jpg"  # Set the image name to "apod.jpg"
            image_path = os.path.join("/media", image_name)  # Specify the path where to save the image

            with open(image_path, 'wb') as file:
                file.write(response.content)

            return image_path  # Return the filepath of the downloaded image
        else:
            print("Failed to download image.")
            return None
    else:
        print("Image not found.")
        return None


def get_video_url():
    try:
        iframe_tag = soup.find('iframe')

        if iframe_tag:
            # Extract the src attribute from the iframe tag
            video_url = iframe_tag['src']
            return video_url
        else:
            print("No video iframe found.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_video(video_url, output_path="/media/apod_video.mp4"):
    try:
        # Set up yt-dlp options for downloading
        ydl_opts = {
            'outtmpl': output_path,  # Define the output file name
            'format': 'best',        # Download the best quality video
        }

        # Create an yt-dlp instance and download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print(f"Video successfully downloaded to {output_path}")
        return output_path  # Return the path of the downloaded video
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return None  # Return None if an error occurs
