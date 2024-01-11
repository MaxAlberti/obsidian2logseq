import re
import os


class ObsidianLink:
    text: str
    content: str

    def __init__(self, text, content):
        self.text = text
        self.content = content


def main():
    print("Please select your logseq folder with files to change.")
    logseq_dir = input("Input: ")
    # print(logseq_dir)
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
            print(f"Converting '{f.name}'...")
            file_content = ""
            with open(f.path, mode="r") as file:
                file_content = file.read()
            image_links, exca_links, other_links = extract_links(
                file_content, page_names
            )
            new_content = file_content
            for link in image_links:
                new_content = new_content.replace(
                    link.text, str(convert_image_link(link))
                )
            for link in exca_links:
                new_content = new_content.replace(
                    link.text, str(convert_excalidraw_link(link, page_names))
                )
            for link in other_links:
                new_content = new_content.replace(link.text, link.text[1:])
            with open(f.path, mode="w") as file:
                file.write(new_content)


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
            image_links.add(ObsidianLink(link, link_content))
        elif (
            link_content.endswith(".excalidraw")
            or link_content + ".excalidraw.md" in page_names
            or link_content + ".excalidraw" in page_names
        ):
            exca_links.add(ObsidianLink(link, link_content))
        else:
            other_links.add(ObsidianLink(link, link_content))

    return list(image_links), list(exca_links), list(other_links)


def convert_image_link(image_link: ObsidianLink) -> str:
    link_name = image_link.content
    return f"![{link_name}](../assets/{image_link.content})"


def convert_excalidraw_link(exca_link: ObsidianLink, page_names: list) -> str:
    link_name = exca_link.content
    if link_name.endswith(".excalidraw"):
        link_name = link_name[:-11]
    elif link_name.endswith(".excalidraw.md"):
        link_name = link_name[:-14]
    elif link_name.endswith(".md"):
        link_name = link_name[:-3]
    return f"{{{{renderer excalidraw, {link_name}}}}}"


if __name__ == "__main__":
    main()
