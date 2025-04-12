import csv

def save_links_to_file(links, filename="dubai_buildings_links.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Building URL"]) 
        for link in links:
            writer.writerow([link]) 
