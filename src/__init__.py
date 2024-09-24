from __future__ import annotations

import json
from typing import Literal

LANGUAGES = Literal["hindi", "english", "sanskrit"]
VALID_NAMES = ["chapters", "verses", "commentaries", "translations"]
VALID_NAMES_HINT = Literal["chapters", "verses", "commentaries", "translations"]


class Commentary:
    def __init__(
        self,
        *,
        authorName: str,
        author_id: int,
        description: str,
        id: int,
        lang: str,
        language_id: int,
        verseNumber: int,
        verse_id: int,
    ):
        self.id = id
        self.author_id = author_id
        self.language_id = language_id
        self.verse_id = verse_id

        self.author_name = authorName
        self.description = description
        self.lang = lang
        self.verse_number = verseNumber


class Chapter:
    def __init__(
        self,
        *,
        id: int,
        chapter_number: int,
        chapter_summary: str,
        chapter_summary_hindi: str,
        image_name: str,
        name: str,
        name_meaning: str,
        name_translation: str,
        name_transliterated: str,
        verses_count: int,
    ):
        self.id = id
        self.chapter_number = chapter_number
        self.chapter_summary = chapter_summary
        self.chapter_summary_hindi = chapter_summary_hindi
        self.image_name = image_name
        self.name = name
        self.name_meaning = name_meaning
        self.name_translation = name_translation

        self.verses_count = verses_count
        self.name_transliterated = name_transliterated

        self._verses: list[Verse] = []

    @property
    def verses(self) -> list[Verse]:
        return self._verses

    @verses.setter
    def verses(self, value: list[Verse]) -> None:
        self._verses = value


class Translation:
    def __init__(
        self,
        *,
        authorName: str,
        author_id: int,
        description: str,
        id: int,
        lang: str,
        language_id: int,
        verseNumber: int,
        verse_id: int,
    ):
        self.id = id
        self.author_id = author_id
        self.language_id = language_id
        self.verse_id = verse_id

        self.author_name = authorName
        self.description = description
        self.lang = lang
        self.verse_number = verseNumber

        self._verse: Verse | None = None

    @property
    def text(self) -> str:
        return self.description

    @property
    def verse(self) -> Verse | None:
        return self._verse

    @verse.setter
    def verse(self, value: Verse) -> None:
        self._verse = value


class Verse:
    def __init__(
        self,
        *,
        chapter_id: int,
        chapter_number: int,
        externalId: int,
        id: int,
        text: str,
        title: str,
        verse_number: int,
        verse_order: int,
        transliteration: str,
        word_meanings: str,
    ):
        self.id = id

        self.chapter_id = chapter_id
        self.chapter_number = chapter_number

        self.external_id = externalId
        self.text = text

        self.title = title

        self.verse_number = verse_number
        self.verse_order = verse_order
        self.transliteration = transliteration
        self.word_meanings = word_meanings

        self._translations: dict[int, Translation] = {}
        self._chapter: Chapter | None = None

    @property
    def chapter(self) -> Chapter | None:
        return self._chapter

    @chapter.setter
    def chapter(self, value: Chapter) -> None:
        self._chapter = value

    def __str__(self):
        return f"{self.chapter_number}:{self.verse_number} - {self.text}"

    def get_translation(self, *, language: LANGUAGES) -> Translation | None:
        mapper = {
            "hindi": 1,
            "english": 2,
            "sanskrit": 3,
        }
        return self._translations.get(mapper[language], None)


class Geeta:
    chapters: list[Chapter]
    verses: list[Verse]
    commentaries: list[Commentary]
    translations: list[Translation]

    mapper = {
        "chapters": Chapter,
        "verses": Verse,
        "commentaries": Commentary,
        "translations": Translation,
    }

    def __init__(self) -> None:
        self.chapters = []
        self.verses = []
        self.commentaries = []
        self.translations = []

        for name in VALID_NAMES:
            self.load_data(
                name=name,
                cls=self.mapper[name],
                file_path=f"src/data/{name}.json",
            )

        self.chapters = sorted(self.chapters, key=lambda x: x.chapter_number)
        self.verses = sorted(self.verses, key=lambda x: x.verse_order)

        self.set_translations()
        self.set_chapters()
        self.set_verses()

    def load_data(self, *, name: VALID_NAMES_HINT, cls: type, file_path: str) -> None:
        with open(file_path, "r") as file:
            data = json.load(file)

            setattr(self, name, [cls(**item) for item in data])

    def set_translations(self) -> None:
        for translation in self.translations:
            verse = self.verses[translation.verse_id - 1]
            verse._translations[translation.language_id] = translation

            translation.verse = verse

    def set_chapters(self) -> None:
        for verse in self.verses:
            verse.chapter = self.chapters[verse.chapter_id - 1]

    def set_verses(self) -> None:
        for chapter in self.chapters:
            chapter.verses = [
                verse for verse in self.verses if verse.chapter_id == chapter.id
            ]

    def search(
        self, *, chapter_number: int, verse_number: int, language: LANGUAGES
    ) -> Translation | None:
        return next(
            (
                verse.get_translation(language=language)
                for verse in self.verses
                if verse.chapter_number == chapter_number
                and verse.verse_number == verse_number
            ),
            None,
        )


GEETA = Geeta()
