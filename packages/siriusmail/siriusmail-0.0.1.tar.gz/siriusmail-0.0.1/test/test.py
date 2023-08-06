import re
import unittest

from siriusmail.rtf_extractor import remove_rtf


class RemoveRTFRegex(unittest.TestCase):

    def test_rtf_remove(self):
        before_text = r"""
            {\rtf1\ansi\ansicpg1252\fromhtml1 \fbidis \deff0{\fonttbl
            {\f0\fswiss\fcharset0 Arial;}
            {\f1\fmodern Courier New;}
            {\f2\fnil\fcharset2 Symbol;}
            {\f3\fmodern\fcharset0 Courier New;}}
            {\colortbl\red0\green0\blue0;\red0\green0\blue255;}
            \uc1\pard\plain\deftab360 \f0\fs24
            {\*\htmltag19 <html>}
            {\*\htmltag34 <head>}
            {\*\htmltag1 \par }
            {\*\htmltag1 \par }
            {\*\htmltag241 <style type="text/css" style="display:none;">}
            {\*\htmltag241  P \{margin-top:0;margin-bottom:0;\} }
            {\*\htmltag249 </style>}
            {\*\htmltag1 \par }
            {\*\htmltag41 </head>}
            {\*\htmltag2 \par }
            {\*\htmltag50 <body dir="ltr">}\htmlrtf \ltrdoc\ltrpar\ql\ltrch \htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div style="font-family: Calibri, Arial, Helvetica, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div class="_2Qk4AbDuWwkuLB005ds2jm QMubUjbS-BOly_BTHEZj7 allowTextSelection">}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div lang="en-US">}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 FIXTURES PAST PRESENT FUTURE
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 MAX
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 MIN
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 AVG
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0
            {\*\htmltag84 &nbsp;}\htmlrtf \'a0\htmlrtf0
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 HELLO INTRODUCTIONS
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0
            {\*\htmltag84 &nbsp;}\htmlrtf \'a0\htmlrtf0
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <table style="border-collapse:collapse">}\htmlrtf {\pard\plain \f0\fs24 \htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <tbody>}
            {\*\htmltag0 \par }
            {\*\htmltag64 <tr>}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border:1pt solid #ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}HEADER1\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:solid solid solid none;border-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 HEADER2
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:solid solid solid none;border-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 HEADER3
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:solid solid solid none;border-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 HEADER4
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }
            {\*\htmltag72 </tr>}
            {\*\htmltag0 \par }
            {\*\htmltag64 <tr>}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:none solid solid solid;border-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 1
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 2
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 3
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 4
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }
            {\*\htmltag72 </tr>}
            {\*\htmltag0 \par }
            {\*\htmltag64 <tr>}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:none solid solid solid;border-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 5
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 6
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 7
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }{\*\htmltag64}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">}\htmlrtf {\htmlrtf0
            {\*\htmltag4 \par }{\*\htmltag72}
            {\*\htmltag68 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}
            {\*\htmltag148 <span style="color:black">}\htmlrtf {\htmlrtf0 8
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag248 </td>}
            {\*\htmltag0 \par }
            {\*\htmltag72 </tr>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </tbody>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </table>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0
            {\*\htmltag84 &nbsp;}\htmlrtf \'a0\htmlrtf0
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0
            {\*\htmltag84 &nbsp;}\htmlrtf \'a0\htmlrtf0
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 TEST
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 TEST
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag96 <div>}\htmlrtf {\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag64 <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">}\htmlrtf {\htmlrtf0
            {\*\htmltag148 <span style="color:black;font-size:12pt">}\htmlrtf {\htmlrtf0 END
            {\*\htmltag156 </span>}\htmlrtf }\htmlrtf0 \htmlrtf\par}\htmlrtf0
            \htmlrtf \par
            \htmlrtf0
            {\*\htmltag72 </p>}
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag112 <br>}\htmlrtf \par
            \htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag104 </div>}\htmlrtf }\htmlrtf0
            {\*\htmltag0 \par }
            {\*\htmltag58 </body>}
            {\*\htmltag2 \par }
            {\*\htmltag27 </html>}
            {\*\htmltag3 \par }}
        """
        after_text = """
            rtf1ansiansicpg1252  deff0 Arial; Courier New; Symbol; Courier New;colortblred0green0blue0;red0green0blue255;uc1deftab360   <html> <head>     <style type="text/css" style="display:none;">  P margin-top:0;margin-bottom:0;  </style>   </head>   <body dir="ltr"> ltrdocltrpar     <div style="font-family: Calibri, Arial, Helvetica, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">     <div class="_2Qk4AbDuWwkuLB005ds2jm QMubUjbS-BOly_BTHEZj7 allowTextSelection">     <div>     <div>     <div lang="en-US">     <div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  FIXTURES PAST PRESENT FUTURE </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  MAX </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  MIN </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  AVG </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">   &nbsp; 'a0  </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  HELLO INTRODUCTIONS </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">   &nbsp; 'a0  </span>     </p>   </div>     <div>     <div>     <div>     <table style="border-collapse:collapse">       <tbody>   <tr>     <td style="background-color:white;width:90pt;padding:0.75pt;border:1pt solid #ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">HEADER1     </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:solid solid solid none;border-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  HEADER2 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:solid solid solid none;border-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  HEADER3 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:solid solid solid none;border-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  HEADER4 </span>       </p>   </td>   </tr>   <tr>     <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:none solid solid solid;border-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  1 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  2 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  3 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  4 </span>       </p>   </td>   </tr>   <tr>     <td style="background-color:white;width:90pt;padding:0.75pt;border-width:1pt;border-style:none solid solid solid;border-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  5 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  6 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  7 </span>       </p>   </td>     <td style="background-color:white;width:90pt;padding:0.75pt;border-style:none solid solid none;border-right-width:1pt;border-bottom-width:1pt;border-right-color:#ABABAB;border-bottom-color:#ABABAB">     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0"> <span style="color:black">  8 </span>       </p>   </td>   </tr>   </tbody>   </table>     </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">   &nbsp; 'a0  </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">   &nbsp; 'a0  </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  TEST </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  TEST </span>     </p>   </div>     <div>     <p style="font-size:11pt;font-family:Calibri,sans-serif;margin:0">   <span style="color:black;font-size:12pt">  END </span>     </p>   </div>     </div>     </div>     </div>     </div>     </div>     </div>     </div>     <br>     </div>     </body>   </html>
        """
        self.assertEqual(
            re.sub(r"[\n\s]+", "", remove_rtf(before_text)),
            re.sub(r"[\n\s]+", "", after_text),
        )
        

if __name__ == '__main__':
    unittest.main()
