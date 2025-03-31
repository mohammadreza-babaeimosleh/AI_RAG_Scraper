def save_links_to_file(links, filename="dubai_buildings_links.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
