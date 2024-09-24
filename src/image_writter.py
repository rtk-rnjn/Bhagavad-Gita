from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from src import GEETA

FONT = r"src/fonts/TiroDevanagariSanskrit-Regular.ttf"
BOX = {
    "x": 78,
    "y": 798,
    "width": 945,
    "height": 241,
}

class ImageWritter:
    TEMPLATE_IMAGE = r"src/assets/template.jpg"
    BACKGROUND_IMAGE = r"src/assets/background.jpg"

    def __init__(self) -> None:
        self.font = ImageFont.truetype(FONT, 31)

    def write_template(
        self,
        *,
        chapter_number: int,
        verse_number: int,
        language: str,
        center_align: bool = True,
    ) -> None:
        translation = GEETA.search(
            chapter_number=chapter_number, verse_number=verse_number, language=language
        )

        if translation is None:
            return

        verse = translation.verse

        if verse is None:
            return

        image = Image.open(self.TEMPLATE_IMAGE)
        draw = ImageDraw.Draw(image)

        verse_text = verse.text

        if center_align:
            verse_text = self.center_align(verse_text)

        x = BOX["x"] + BOX["width"] // 2
        y = BOX["y"] + BOX["height"] // 2 + 10

        draw.text(
            (x, y),
            verse_text,
            font=self.font,
            fill="black",
            anchor="mm",
            align="center",
        )

        image.save(f"output/{chapter_number}_{verse_number}_{language}.png")

    def write_background(
        self,
        *,
        chapter_number: int,
        verse_number: int,
        language: str = "english",
        center_align: bool = True,
    ) -> None:
        self.font = ImageFont.truetype(FONT, 170)
        image = Image.open(self.BACKGROUND_IMAGE)
        image = image.filter(ImageFilter.GaussianBlur(10))

        translation = GEETA.search(
            chapter_number=chapter_number, verse_number=verse_number, language=language
        )

        if translation is None:
            return

        verse = translation.verse

        if verse is None:
            return
        
        verse_text = verse.text

        if center_align:
            verse_text = self.center_align(verse_text)

        draw = ImageDraw.Draw(image)

        image_x, image_y = image.size

        x = (image_x) // 2
        y = (image_y) // 2

        draw.text(
            (x, y - 300),
            verse_text,
            font=self.font,
            fill="white",
            anchor="mm",
            align="center",
        )

        draw.text(
            (x, y + 300),
            f"Chapter {chapter_number}, Verse {verse_number}",
            font=self.font,
            fill="white",
            anchor="mm",
            align="center",
        )

        translation_text = self.center_align(translation.description)

        print(image_y)

        draw.text(
            (x, y + 2000),
            self.wrap_text_center(translation_text),
            font=self.font,
            fill="white",
            anchor="mm",
            align="center",
        )

        image.save("output/background.png")

    def center_align(self, text: str) -> str:
        texts = text.split("\n")

        max_len = max(map(len, texts))

        return "\n".join([f"{t:^{max_len}}" for t in texts])
    
    def wrap_text_center(self, text: str, width: int = 30) -> str:
        texts = text.split("\n")

        new_texts = []

        for t in texts:
            if len(t) > width:
                new_texts.extend([t[i : i + width] for i in range(0, len(t), width)])
            else:
                new_texts.append(t)

        return "\n".join(new_texts)