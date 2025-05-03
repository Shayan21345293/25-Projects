import requests
from bs4 import BeautifulSoup

def get_github_profile_image_url(username):
    # URL of the GitHub profile page
    url = f"https://github.com/{username}"
    
    # Send a GET request to fetch the content of the page
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the profile image tag (typically within <img> tag with class 'avatar-user')
        avatar = soup.find('img', {'class': 'avatar-user'})
        
        if avatar:
            # Get the 'src' attribute of the image tag (which contains the image URL)
            image_url = avatar['src']
            return image_url
        else:
            print("Profile image not found.")
            return None
    else:
        print("Could not retrieve the page.")
        return None

if __name__ == "__main__":
    username = input("Please enter the GitHub user URL: ")
    
    # Extract the username from the full URL if necessary
    if "https://github.com/" in username:
        username = username.replace("https://github.com/", "")
    
    profile_image_url = get_github_profile_image_url(username)
    
    if profile_image_url:
        print("Profile Image URL:", profile_image_url)
    else:
        print("Could not retrieve profile image.")
