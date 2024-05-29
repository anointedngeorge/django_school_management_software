from bs4 import BeautifulSoup

html_content = ""
# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract class names from <i> tags
icon_tags = soup.find_all('i')
class_names = [f"{icon['class'][0]} {icon['class'][1]}" for icon in icon_tags]

# print(class_names)
# Format into Django CharField choices [(value, display_value)]
django_choices = [(class_name, class_name.upper()) for class_name in class_names]

# Print Django CharField choices
print(django_choices)