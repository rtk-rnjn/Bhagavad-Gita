from src.image_writter import ImageWritter


def main():
    image_writter = ImageWritter()

    image_writter.write_background(chapter_number=1, verse_number=1)


if __name__ == "__main__":
    main()
