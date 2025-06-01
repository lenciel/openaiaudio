
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import logging
from datetime import timedelta

logger = logging.getLogger('correct_srt')
hdlr = logging.FileHandler('correct_srt.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


def rename_folders():
    """
    Rename folders in the 'inputs/txts' directory based on a predefined mapping.
    Each folder is renamed to its corresponding book index and short name.
    """
    # Dictionary mapping book names to their short names and index numbers
    book_mapping = {
        '1. GENESIS': ('GEN', 1),
        '2. EXODUS': ('EXO', 2),
        '3. LEVITICUS': ('LEV', 3),
        '4. NUMBERS': ('NUM', 4),
        '5. DEUTERONOMY': ('DEU', 5),
        '6. JOSHUA': ('JOS', 6),
        '7. JUDGES': ('JUD', 7),
        '8. RUTH': ('RUT', 8),
        '9. 1SAMUEL': ('1SA', 9),
        '10. 2SAMUEL': ('2SA', 10),
        '11. 1KINGS': ('1KI', 11),
        '12. 2KINGS': ('2KI', 12),
        '13. 1CHRONICLES': ('1CH', 13),
        '14. 2CHRONICLES': ('2CH', 14),
        '15. EZRA': ('EZR', 15),
        '16. NEHEMIAH': ('NEH', 16),
        '17. ESTHER': ('EST', 17),
        '18. JOB': ('JOB', 18),
        '19. PSALMS': ('PSA', 19),
        '20. PROVERBS': ('PRO', 20),
        '21. ECCLESIASTES': ('ECC', 21),
        '22. SONGOFSOLOMON': ('SON', 22),
        '23. ISAIAH': ('ISA', 23),
        '24. JEREMIAH': ('JER', 24),
        '25. LAMENTATIONS': ('LAM', 25),
        '26. EZEKIEL': ('EZE', 26),
        '27. DANIEL': ('DAN', 27),
        '28. HOSEA': ('HOS', 28),
        '29. JOEL': ('JOE', 29),
        '30. AMOS': ('AMO', 30),
        '31. OBADIAH': ('OBA', 31),
        '32. JONAH': ('JON', 32),
        '33. MICAH': ('MIC', 33),
        '34. NAHUM': ('NAH', 34),
        '35. HABAKKUK': ('HAB', 35),
        '36. ZEPHANIAH': ('ZEP', 36),
        '37. HAGGAI': ('HAG', 37),
        '38. ZECHARIAH': ('ZEC', 38),
        '39. MALACHI': ('MAL', 39),
        '40. MATTHEW': ('MAT', 40),
        '41. MARK': ('MAR', 41),
        '42. LUKE': ('LUK', 42),
        '43. JOHN': ('JOH', 43),
        '44. ACTS': ('ACT', 44),
        '45. ROMANS': ('ROM', 45),
        '46. 1CORINTHIANS': ('1CO', 46),
        '47. 2CORINTHIANS': ('2CO', 47),
        '48. GALATIANS': ('GAL', 48),
        '49. EPHESIANS': ('EPH', 49),
        '50. PHILIPPIANS': ('PHI', 50),
        '51. COLOSSIANS': ('COL', 51),
        '52. 1THESSALONIANS': ('1TH', 52),
        '53. 2THESSALONIANS': ('2TH', 53),
        '54. 1TIMOTHY': ('1TI', 54),
        '55. 2TIMOTHY': ('2TI', 55),
        '56. TITUS': ('TIT', 56),
        '57. PHILEMON': ('PHE', 57),
        '58. HEBREWS': ('HEB', 58),
        '59. JAMES': ('JAM', 59),
        '60. 1PETER': ('1PE', 60),
        '61. 2PETER': ('2PE', 61),
        '62. 1JOHN': ('1JO', 62),
        '63. 2JOHN': ('2JO', 63),
        '64. 3JOHN': ('3JO', 64),
        '65. JUDE': ('JUD', 65),
        '66. REVELATION': ('REV', 66)
    }

    # # Dictionary mapping book names to their short names and index numbers
    # book_mapping = {
    #     'Genesis': ('GEN', 1),
    #     'Exodus': ('EXO', 2),
    #     'Leviticus': ('LEV', 3),
    #     'Numbers': ('NUM', 4),
    #     'Deuteronomy': ('DEU', 5),
    #     'Joshua': ('JOS', 6),
    #     'Judges': ('JUD', 7),
    #     'Ruth': ('RUT', 8),
    #     '1 Samuel': ('1SA', 9),
    #     '2 Samuel': ('2SA', 10),
    #     '1 Kings': ('1KI', 11),
    #     '2 Kings': ('2KI', 12),
    #     '1 Chronicles': ('1CH', 13),
    #     '2 Chronicles': ('2CH', 14),
    #     'Ezra': ('EZR', 15),
    #     'Nehemiah': ('NEH', 16),
    #     'Esther': ('EST', 17),
    #     'Job': ('JOB', 18),
    #     'Psalms': ('PSA', 19),
    #     'Proverbs': ('PRO', 20),
    #     'Ecclesiastes': ('ECC', 21),
    #     'Song of Solomon': ('SON', 22),
    #     'Isaiah': ('ISA', 23),
    #     'Jeremiah': ('JER', 24),
    #     'Lamentations': ('LAM', 25),
    #     'Ezekiel': ('EZE', 26),
    #     'Daniel': ('DAN', 27),
    #     'Hosea': ('HOS', 28),
    #     'Joel': ('JOE', 29),
    #     'Amos': ('AMO', 30),
    #     'Obadiah': ('OBA', 31),
    #     'Jonah': ('JON', 32),
    #     'Micah': ('MIC', 33),
    #     'Nahum': ('NAH', 34),
    #     'Habakkuk': ('HAB', 35),
    #     'Zephaniah': ('ZEP', 36),
    #     'Haggai': ('HAG', 37),
    #     'Zechariah': ('ZEC', 38),
    #     'Malachi': ('MAL', 39),
    #     'Matthew': ('MAT', 40),
    #     'Mark': ('MAR', 41),
    #     'Luke': ('LUK', 42),
    #     'John': ('JOH', 43),
    #     'Acts': ('ACT', 44),
    #     'Romans': ('ROM', 45),
    #     '1 Corinthians': ('1CO', 46),
    #     '2 Corinthians': ('2CO', 47),
    #     'Galatians': ('GAL', 48),
    #     'Ephesians': ('EPH', 49),
    #     'Philippians': ('PHI', 50),
    #     'Colossians': ('COL', 51),
    #     '1 Thessalonians': ('1TH', 52),
    #     '2 Thessalonians': ('2TH', 53),
    #     '1 Timothy': ('1TI', 54),
    #     '2 Timothy': ('2TI', 55),
    #     'Titus': ('TIT', 56),
    #     'Philemon': ('PHE', 57),
    #     'Hebrews': ('HEB', 58),
    #     'James': ('JAM', 59),
    #     '1 Peter': ('1PE', 60),
    #     '2 Peter': ('2PE', 61),
    #     '1 John': ('1JO', 62),
    #     '2 John': ('2JO', 63),
    #     '3 John': ('3JO', 64),
    #     'Jude': ('JUD', 65),
    #     'Revelation': ('REV', 66)
    # }

    base_path = 'inputs/audios'

    # Iterate through all folders in the base directory
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            # Check if the folder name exists in our mapping
            if folder_name in book_mapping:
                short_name, index = book_mapping[folder_name]
                new_name = f"{index}.{short_name}"
                new_path = os.path.join(base_path, new_name)

                # Rename the folder
                try:
                    os.rename(folder_path, new_path)
                    print(f"Renamed {folder_name} to {new_name}")
                except Exception as e:
                    print(f"Error renaming {folder_name}: {str(e)}")


def rename_files():
    base_path = 'inputs/txts'
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            # Extract letters from folder name
            folder_letters = ''.join(c for c in folder if c.isalpha())

            # Process each file in the folder
            for filename in os.listdir(folder_path):
                if filename.endswith('.txt'):
                    # Extract numbers from filename
                    file_numbers = ''.join(
                        c for c in filename if c.isdigit())

                    # Create new filename
                    new_filename = f"{folder_letters}{file_numbers}.txt"
                    old_file_path = os.path.join(folder_path, filename)
                    new_file_path = os.path.join(folder_path, new_filename)

                    try:
                        os.rename(old_file_path, new_file_path)
                        print(f"Renamed {filename} to {new_filename}")
                    except Exception as e:
                        print(f"Error renaming {filename}: {str(e)}")


def parse_srt_time(s):
    h, m, rest = s.split(':')
    s, ms = rest.split(',')
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))


def format_srt_time(td):
    total_seconds = int(td.total_seconds())
    ms = td.microseconds // 1000
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def parse_srt(file_content):
    pattern = r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+([\s\S]+?)(?=\n\d+\n|\Z)'
    return [
        {
            "index": int(m[0]),
            "start": parse_srt_time(m[1]),
            "end": parse_srt_time(m[2]),
            "text": m[3].strip().replace('\n', ' ')
        }
        for m in re.findall(pattern, file_content)
    ]


def parse_verses(file_content):
    verses = re.findall(r'(?m)^(\d+)\s+(.*?)(?=\n\d+\s|\Z)',
                        file_content, re.DOTALL)
    return {int(num): text.replace('\n', ' ').strip() for num, text in verses}


def is_text_subset(text_a: str, text_b: str) -> bool:
    # Split texts into words and convert to lowercase
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())

    # Determine which set is smaller
    shorter_set = words_a if len(words_a) <= len(words_b) else words_b
    longer_set = words_b if len(words_a) <= len(words_b) else words_a

    if not shorter_set:
        return False

    # Count how many words from shorter text appear in longer text
    common_words = shorter_set.intersection(longer_set)
    similarity_ratio = len(common_words) / len(shorter_set)

    return similarity_ratio >= 0.6


def merge_srt_by_verses(srt_entries, verses):
    merged = []
    srt_entries = srt_entries.copy()  # Create a copy to modify

    for verse_num, verse_text in verses.items():
        verse_text_clean = re.sub(r'[^\w\s]', '', verse_text).lower()
        current_entry = {
            "index": verse_num,
            "start": None,
            "end": None,
            "text": verse_text
        }

        i = 0
        while i < len(srt_entries):
            entry = srt_entries[i]
            entry_text_clean = re.sub(r'[^\w\s]', '', entry["text"]).lower()

            logger.debug(
                f"Checking entry {srt_entries.index(entry)}: {entry_text_clean} against verse: {verse_num} {verse_text_clean}")

            if is_text_subset(entry_text_clean, verse_text_clean):
                if current_entry["start"] is None:
                    current_entry["start"] = entry["start"]
                    logger.debug(
                        f"Updated current_entry start to: {entry["start"]} for verse {verse_num}")
                current_entry["end"] = entry["end"]
                logger.debug(
                    f"Updated current_entry end to: {entry["end"]} for verse {verse_num}")
                srt_entries.pop(i)  # Remove the matched entry
                continue  # Continue checking next entry for this verse
            else:
                break  # Exit loop and move to next verse

            i += 1
        if current_entry["start"] is not None and current_entry["end"] is not None:
            merged.append(current_entry)

    return merged


def generate_srt(entries):
    result = ""
    for entry in entries:
        result += f"{entry['index']}\n"
        result += f"{format_srt_time(entry['start'])} --> {format_srt_time(entry['end'])}\n"
        result += f"{entry['text']}\n\n"
    return result.strip()


def generate_srt_from_files(input_srt, input_verses, output_srt):
    """
    Generate a merged SRT file from the SRT and verses text files.
    This function reads the SRT file and the verses text file, processes them,
    and writes the merged content to a new SRT file.
    """
    # Load files
    with open(input_srt, "r", encoding="utf-8") as srt_file:
        srt_content = srt_file.read()

    with open(input_verses, "r", encoding="utf-8") as txt_file:
        verses_content = txt_file.read()

    # Process
    srt_entries = parse_srt(srt_content)
    verses = parse_verses(verses_content)
    merged_srt = merge_srt_by_verses(srt_entries, verses)
    final_srt = generate_srt(merged_srt)

    # Save result
    with open(output_srt, "w", encoding="utf-8") as out_file:
        out_file.write(final_srt)


if __name__ == "__main__":
    # rename_foldes()
    # rename_files()

    # generate_srt_from_files(
    #     "inputs/audios/1.GEN/GEN1.mp3.srt", "inputs/audios/1.GEN/GEN1.txt", "outputs/GEN1_merged.srt")
    # generate_srt_from_files(
    #     "inputs/audios/5.DEU/DEU1.mp3.srt", "inputs/audios/5.DEU/DEU1.txt", "outputs/DEU1_merged.srt")
    # generate_srt_from_files(
    #     "inputs/audios/5.DEU/DEU2.mp3.srt", "inputs/audios/5.DEU/DEU2.txt", "outputs/DEU2_merged.srt")

    base_path = 'inputs/audios'
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            # Process each file in the folder
            for filename in os.listdir(folder_path):
                if filename.endswith('.srt'):
                    # Get the base name without extension
                    base_name = os.path.splitext(filename)[0].split('.')[0]

                    # Construct paths
                    srt_path = os.path.join(
                        folder_path, f"{base_name}.mp3.srt")
                    txt_path = os.path.join(folder_path, f"{base_name}.txt")
                    output_path = os.path.join(
                        folder_path, f"{base_name}_merged.srt")
                    logger.debug(f"Processing srt_path {srt_path}...")
                    logger.debug(f"Processing txt_path {txt_path}...")
                    logger.debug(f"Processing output_path {output_path}...")
                    # Generate merged srt if txt file exists
                    if os.path.exists(txt_path):
                        try:
                            logger.info(
                                f"Generating merged SRT for {filename}")
                            generate_srt_from_files(
                                srt_path, txt_path, output_path)
                        except Exception as e:
                            logger.error(
                                f"Error processing {filename}: {str(e)}")
                    else:
                        logger.error(
                            f"No matching text file found for {filename}")
