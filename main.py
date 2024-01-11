import re
import os


def main():
    print("Please select your logseq folder with files to change.")
    logseq_dir = input("Input: ")
    print(logseq_dir)
    if logseq_dir.startswith('"'):
        logseq_dir = logseq_dir[1:]
    if logseq_dir.endswith('"'):
        logseq_dir = logseq_dir[:-1]
    if not os.path.exists(logseq_dir):
        print("Folder doesn't exist!")
        return
    pages_dir = os.path.join(logseq_dir, "pages")
    if not os.path.exists(pages_dir):
        print("Sub-Folder /pages  doesn't exist!")
        return

    pages = []
    page_names = []
    for f in os.scandir(pages_dir):
        if not f.is_dir() and f.name.endswith(".md"):
            pages.append(f)
            page_names.append(f.name)

    for f in pages:
        if ".excalidraw." not in f.name:
            file_content = ""
            with open(f.path, mode="r") as file:
                file_content = file.read()
            image_links, exca_links, other_links = extract_links(
                file_content, page_names
            )
            print(image_links)
            print(exca_links)
            print(other_links)
            input("--------")


def extract_links(text: str, page_names: list):
    """
    Links need to have the format ![[content]]
    Returns image_links, exca_links, other_links"""
    image_links = set()
    exca_links = set()
    other_links = set()

    regex = r"(!\[\[([^\]]+)\]\])"

    matches = re.finditer(regex, text, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        link = match.group(0)
        link_content = match.group(2)
        if (
            link_content.endswith(".png")
            or link_content.endswith(".jpg")
            or link_content.endswith(".jpeg")
            or link_content.endswith(".webp")
            or link_content.endswith(".svg")
        ):
            image_links.add(link)
        elif (
            link_content.endswith(".excalidraw")
            or link_content + ".excalidraw.md" in page_names
            or link_content + ".excalidraw" in page_names
        ):
            exca_links.add(link)
        else:
            other_links.add(link)

    return list(image_links), list(exca_links), list(other_links)


if __name__ == "__main__":
    main()
