# siriusmail
For all those mails

## ✨ Highlight

✔️ Email parser for both outlook .msg files and regular .eml files

✔️ Use our built in rtf regex parser to remove rtf tags or use your own

### 📦️ Installation
```sh
pip install siriusmail

```

### 📝 Examples

```python
from siriusmail.parser import ParseEmail
from siriusmail.rtf_extractor import remove_rtf

FILE = r"INPUT_FILEPATH"
OUT = r"OUTPUT_FILEPATH"
ENCODING = "encoding" # optional, you may specify if you are aware of the encoding being used, else chardet will try to guess

# 3 retrieval options here - body, text or attachments
msg = ParseEmail(FILE).process_streams("body", encoding=ENCODING)
msg = ParseEmail(FILE).process_streams("text")
msg = ParseEmail(FILE).process_streams("attachments", filepath=OUT)

# use our simple regex extractor to remove rtf tags
ADDITIONAL_TAGS = [r"(\\+pard)", r"(\\+pard1)",] # optional, we are definitely missing rtf tags since this is a "hardcoded" solution, add more tags or raise an issue!
msg = remove_rtf(msg, extra_tags=ADDITIONAL_TAGS)

```

### 🚀 Releases and To-Dos
- Make RTF deencapsulation more robust
- Add test for specific emails [not available at the moment due to personal emails]
