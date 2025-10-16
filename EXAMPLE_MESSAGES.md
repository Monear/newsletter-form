# Example Writing Info Messages

This document shows what students will see in the "Writing Info:" field across both sessions.

## Session 1: Initial Instructions

**All students see this in Session 1:**

```
By the end of this class you should write around 250 words.
```

You can customize this message in `config.py` by editing `WRITING_INFO_SESSION_1`.

---

## Session 2: Progress Messages

After Session 1 responses are processed, students will see different messages based on their word count.

### Example 1: Perfect Length

**Student wrote 247 words**

```
Session 1: 247 words written
Good length - you can edit or submit
```

---

### Example 2: Needs More Words

**Student wrote 198 words**

```
Session 1: 198 words written
Add about 52 more words to reach 250
```

---

### Example 3: Too Many Words

**Student wrote 312 words**

```
Session 1: 312 words written
Consider making it shorter by about 62 words
```

---

### Example 4: Way Under

**Student wrote 120 words**

```
Session 1: 120 words written
Add about 130 more words to reach 250
```

---

### Example 5: Way Over

**Student wrote 340 words**

```
Session 1: 340 words written
Consider making it shorter by about 90 words
```

---

### Example 6: Just Under Minimum

**Student wrote 235 words**

```
Session 1: 235 words written
Add about 15 more words to reach 250
```

---

## Word Count Ranges

Defined in `config.py`:

- **WORD_COUNT_MIN**: 240 (below this → "Add more words")
- **WORD_COUNT_TARGET**: 250 (the goal)
- **WORD_COUNT_MAX**: 260 (above this → "Consider shortening")

Students between 240-260 words see: "Good length - you can edit or submit"

## Customization

You can change these messages by editing the `generate_progress_message()` function in `regenerate_links.py` or adjusting the word count ranges in `config.py`.
