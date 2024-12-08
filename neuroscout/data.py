def get_neurips_2024_paper_urls():
    with open("./data/paper_urls.txt") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


NEURIPS_2024_PAPER_URLS = get_neurips_2024_paper_urls()
