import base64
import email
from enum import Enum
import logging
import os
import re
from typing import Dict, Optional, Any

import chardet
from compressed_rtf import compress, decompress
import olefile


logger = logging.getLogger(__name__)


class RetrievalTypes(Enum):
    BODY = "body"
    ATTACHMENT = "attachments"
    TEXT = "text"


class EmailTypes(Enum):
    MSG = "msg"
    EML = "eml"


class ParseEmail:
    def __init__(self, email, *args, **kwargs):
        self.email = email
        self._email_type = self.email.rpartition(".")[-1]

        if self._email_type not in  [item.value for item in EmailTypes]:
            raise KeyError("Invalid file extension, msg or eml only")

        self.attachment_dict = {}
        self.body_data = None
        self.text_data = None

    @staticmethod
    def _determine_encoding(bytestream: bytes, keyed_encoding: Optional[str]) -> str:
        """Use chardet to detect encoding or use user input

        Args:
            bytestream: Email bytes
            keyed_encoding: If user enters a specific encoding

        Returns:
            str:

        """
        if keyed_encoding:
            return keyed_encoding

        en = chardet.detect(bytestream)["encoding"]
        if en:
            return en
        return "ascii"

    @staticmethod
    def _save_files(file_list: Dict[str, Dict[str, str]], folder: str):
        """Save attachments to folder

        Args:
            file_list:
            folder: folder to save
        
        >>> _save_files(
            {
                "id1": {
                    "name": "test1",
                    "stream": "test2",
                },
                "id2": {
                    "name": "test3",
                    "stream": "test4",
                }
            },
            "FOLDER_OUTPUT"
        )
        """
        for k, v in file_list.items():
            attachment_name = v.get("name")
            byte_stream = v.get("stream")
            output = os.path.join(folder, attachment_name)
            with open(output.strip(), "wb") as f:
                b64_de_deets = base64.b64decode(byte_stream)
                f.write(b64_de_deets)

    def _process_msg(self, encoding: str) -> Dict[str, Any]:
        """Strip msg email into components, in a dictionary

        >>> self._process_msg("utf-8")

        Example Output:
            {
                attachment_dict: {
                    "id": {
                        "name": "",
                        "stream": ""
                    }
                }
                body_data: "",
                text_data: "",
            }
        """
        with olefile.OleFileIO(self.email) as ole:
            ole_stream_list = ole.listdir()
            
            for entry in ole_stream_list:
                deets = ole.openstream(entry).read()
                entry_name = "".join(entry)

                # process attachment streams
                if entry_name.startswith("__attach_version1.0") and len(entry) == 2:
                    attachment_id = entry[0].rpartition("_")[-1]

                    if not self.attachment_dict.get(attachment_id):
                        self.attachment_dict[attachment_id] = {
                            "name": None,
                            "stream": None,
                        }
                    # retrieve attachment name
                    if entry[-1] == "__substg1.0_3001001F":
                        en = self._determine_encoding(deets, None)
                        deets = deets.replace(b"\x00", b"")
                        name = deets.decode(en).strip()
                        self.attachment_dict[attachment_id]["name"] = name
                        

                    # retrieve attachment stream
                    if entry[-1] == "__substg1.0_37010102":
                        b64_en_deets = base64.b64encode(deets)
                        self.attachment_dict[attachment_id]["stream"] = b64_en_deets

                # html body
                if entry_name == "__substg1.0_10090102":
                    encode = self._determine_encoding(deets, encoding)
                    decompressed_rtf = decompress(deets)
                    self.body_data = decompressed_rtf.decode(encode)

                # text
                if entry_name == "__substg1.0_1000001F":
                    encode = self._determine_encoding(deets, encoding)
                    self.text_data = deets.decode(encode)

        return {
            "attachments": self.attachment_dict,
            "body_data": self.body_data,
            "text_data": self.text_data,
        }

    def _process_eml(self, encoding: str) -> Dict[str, Any]:
        with open(self.email, "rb") as f:
                self.eml_bytes = email.message_from_bytes(f.read())

        attachment_id = 0
        for part in self.eml_bytes.walk():
            if not encoding:
                encoding = part.get_content_charset()
            content_type = part.get('content-type')

            if part.get_content_subtype() ==  "plain":
                self.text_data = part.get_payload(decode=True).decode(encoding)
            elif part.get_content_subtype() ==  "html":
                self.body_data = part.get_payload(decode=True).decode(encoding)
            elif part.get_filename():
                self.attachment_dict[str(attachment_id)] = {
                    "name": part.get_filename(),
                    "stream": part.get_payload(decode=True),
                }
                attachment_id += 1
            elif part.is_multipart():
                # TODO implement multipart?
                continue
            else:
                continue

        return {
            "attachments": self.attachment_dict,
            "body_data": self.body_data,
            "text_data": self.text_data,
        }


    def process_streams(self, retrieve_type: RetrievalTypes, encoding: Optional[str]=None, folder: Optional[str]=None) -> Any:
        """Main processing command

        Args:
            retrieve_type: Email consists of attachment or text, You may choose to extract text ior attachments
            encoding: For outlook messages, there can be a few encodings that chardet does not parse correctly
            folder: If attachments is chosen in retrieve type

        Returns:
            str or not:

        """
        # process outlook msg/eml file
        if self._email_type == EmailTypes.MSG.value:
            data_item = self._process_msg(encoding)
        elif self._email_type == EmailTypes.EML.value:
            data_item = self._process_eml(encoding)
        else:
            raise ValueError("Not a valid email extension - msg, eml")

        # return data to user
        if retrieve_type == RetrievalTypes.BODY.value:
            return data_item.get("body_data")
        elif retrieve_type == RetrievalTypes.TEXT.value:
            return data_item.get("text_data")
        elif retrieve_type == RetrievalTypes.ATTACHMENT.value:
            if not folder:
                raise ValueError("Folder must be specified for attachments")
            self._save_files(data_item.get("attachments"), folder)
            logger.info(f"Saved items in {folder}")
        else:
            raise ValueError("Not a valid option - text, attachment, body")
