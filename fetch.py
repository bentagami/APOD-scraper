import requests
from bs4 import BeautifulSoup
import os
import re

URL = "https://apod.nasa.gov/apod"
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
        image_url = "https://apod.nasa.gov/" + image_tag['src']  # Complete the image URL

        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Create a directory to save images if it doesn't exist
            os.makedirs("images", exist_ok=True)
            image_name = "apod.jpg"  # Set the image name to "apod.jpg"
            image_path = os.path.join("images", image_name)  # Specify the path where to save the image

            with open(image_path, 'wb') as file:
                file.write(response.content)

            return image_path  # Return the filepath of the downloaded image
        else:
            print("Failed to download image.")
            return None
    else:
        print("Image not found.")
        return None
