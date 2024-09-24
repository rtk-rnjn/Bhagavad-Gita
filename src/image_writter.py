from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from src import GEETA

FONT = r"src/fonts/TiroDevanagariSanskrit-Regular.ttf"


class ImageWritter:
    TEMPLATE_IMAGE = r"src/assets/template.jpg"

    def __init__(self) -> None:
        self.font = ImageFont.truetype(FONT, 31)

    def write(self, *, chapter_number: int, verse_number: int, language: str, text_wrap: bool = True) -> None:
        translation = GEETA.search(chapter_number=chapter_number, verse_number=verse_number, language=language)

        if translation is None:
            return
        
        verse = translation.verse

        if verse is None:
            return
        
        image = Image.open(self.TEMPLATE_IMAGE)
        draw = ImageDraw.Draw(image)

        translation_text = translation.description
        verse_text = verse.text

        if text_wrap:
            translation_text = self.wrap_text(translation_text)
            verse_text = self.wrap_text(verse_text, width=65)

        draw.text((310, 834), verse_text, font=self.font, fill="black")
        draw.text((119, 924), translation_text, font=self.font, fill="black")

        image.save(f"output/{chapter_number}_{verse_number}_{language}.png")
        # TODO
        
    
    def wrap_text(self, text: str, width: int = 60) -> str:
        words = text.split()
        lines = []
        line = []

        for word in words:
            if len(" ".join(line)) + len(word) < width:
                line.append(word)
            else:
                lines.append(" ".join(line))
                line = [word]
        
        lines.append(" ".join(line))

        return "\n".join(lines)