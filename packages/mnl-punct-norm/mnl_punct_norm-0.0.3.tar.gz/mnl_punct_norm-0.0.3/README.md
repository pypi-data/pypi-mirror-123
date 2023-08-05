Useful for removing punctuation marks from various natural languages and from text that may contain non-standard punctuation marks (such as emojis and pictographs). Tested with English, Japanese, Chinese, and Korean.


For the full documentation, please see the repository:

https://github.com/Rairye/mnl-punct-norm


Code sample:

#import functions

from mnl_punct_norm.normalizer import is_punct, strip_punct, replace_punct 

#Half-width period used in English, etc.
print("Half-width period is_punct -> {}".format(is_punct(".")))

#Full-width period used in Japanese, etc.
print("Full-width period is_punct -> {}".format(is_punct("。")))

#Hiragana character
print("Hiragana character is_punct -> {}".format(is_punct("あ")))

#Kanji
print("Kanji character is_punct -> {}".format(is_punct("私")))

#Emoji example
print("★ is_punct -> {}".format(is_punct("★")))

source_str = "This light-weight module, which provides multi-language support, normalizes punctuation in strings."

#Strips all punctuation from source_str.
print(strip_punct(source_str))

#Strips all punctuation from source_str, except for hyphens.
print(strip_punct(source_str, "-"))

#Strips all punctuation from source_str, except for hyphens and commas.
print(strip_punct(source_str, "-,"))

japanese_str = "私は人間（にんげん）です。"

#Strips all punctuation from japanese_str.
print(strip_punct(japanese_str))

#Strips all punctuation from japanese_str, except for parentheses.
print(strip_punct(japanese_str, "（）"))

#Replaces all punctuation in source_str with a half-width space.
print(replace_punct(source_str))

#Replaces all punctuation in source_str with " <PUNCT> ".
print(replace_punct(source_str, replacement = " <PUNCT> "))

#Replaces all punctuation in japanese_str with a full-width space.
print(replace_punct(japanese_str, replacement = "　"))

#String with multiple punctuation marks. The extra spaces in the string are not normalized by the function.
multiple_punct_str = "Wha ... what are you     doing!?!?"

#Example in which multiple punctuation marks are used in a row.
print(replace_punct(multiple_punct_str))

#Example in which multiple punctuation marks are used in a row, with replacement passed as " <PUNCT> ".
print(replace_punct(multiple_punct_str, replacement = " <PUNCT> "))
