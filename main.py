from src.image_writter import ImageWritter


def write_image(chapter_number: int, verse_number: int, language: str) -> None:
    image_writter = ImageWritter()
    image_writter.write_background(
        chapter_number=chapter_number,
        verse_number=verse_number,
        language=language,
        filename=f"{chapter_number}_{verse_number}_{language}.png",
    )


def main():
    write_image(1, 1, "english")


if __name__ == "__main__":
    main()
