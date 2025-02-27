import requests
from bs4 import BeautifulSoup
import pandas as pd

# Harvard Online Courses URL
URL = "https://pll.harvard.edu/subject/computer-science"

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def scrape_courses(url):
    """Scrape Harvard Online Courses for title, description, subject, modality, and links."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to retrieve webpage. Status Code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all course blocks
    courses = soup.find_all("article", class_="content-type--course-instance")

    course_data = []
    for course in courses:
        # Course Title
        title_tag = course.find("h3", class_="field__item")
        title = title_tag.text.strip() if title_tag else "N/A"

        # Course Link
        link_tag = title_tag.find("a") if title_tag else None
        link = f"https://pll.harvard.edu{link_tag['href']}" if link_tag else "N/A"

        # Course Description
        desc_tag = course.find("div", class_="field--name-field-summary")
        description = desc_tag.text.strip() if desc_tag else "N/A"

        # Course Subject
        subject_tag = course.find("div", class_="field--name-extra-field-pll-extra-field-subject")
        subject = subject_tag.text.strip() if subject_tag else "N/A"

        # Modality (Online/In-Person)
        modality_tag = course.find("div", class_="field--name-field-modality")
        modality = modality_tag.text.strip() if modality_tag else "N/A"

        # Append extracted data to list
        course_data.append({
            "Course Title": title,
            "Description": description,
            "Subject": subject,
            "Modality": modality,
            "Course Link": link
        })
    
    return course_data

if __name__ == "__main__":
    courses = scrape_courses(URL)

    if courses:
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(courses)
        df.to_csv("harvard_courses.csv", index=False, encoding="utf-8")

        print("✅ Data successfully saved to harvard_courses.csv\n")
        
        # Print the content of the CSV file
        print(df.to_string(index=False))  # Displays CSV content in a table format
    else:
        print("❌ No courses found. The website structure might have changed.")