"""
Add two directives for .docx elements.
"""

import panflute as pf
from enum import Enum

pagebreak = """<w:p><w:r><w:br w:type="page" /></w:r></w:p>"""

sectionbreak = """<w:p><w:pPr><w:sectPr><w:type w:val="nextPage" /></w:sectPr></w:pPr></w:p>"""

toc = r"""
<w:sdt>
<w:sdtPr>
  <w:docPartObj>
    <w:docPartGallery w:val="Table of Contents" />
  </w:docPartObj>
</w:sdtPr>
<w:sdtContent xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="TOCHeading" />
    </w:pPr>
    <w:r>
      <w:t xml:space="preserve">Table of Contents</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:r>
      <w:fldChar w:fldCharType="begin" w:dirty="true" />
      <w:instrText xml:space="preserve">TOC \o "1-3" \h \z \u</w:instrText>
      <w:fldChar w:fldCharType="separate" />
      <w:fldChar w:fldCharType="end" />
    </w:r>
  </w:p>
</w:sdtContent>
</w:sdt>
"""

# Directives to add
class Cmd:
    NEWPAGE = r"\newpage"
    TOC = r"\toc"
    DOCX = "docx"

directives = {
    Cmd.NEWPAGE: pf.RawBlock(pagebreak, format="openxml"),
    Cmd.TOC: pf.RawBlock(toc, format="openxml")
}

class Docxtras:
    """Enable newpage and toc directives for .docx outputs.
    """

    def action(self, elem, doc):
        if (doc.format == Cmd.DOCX) and isinstance(elem, pf.RawBlock):
            if (elem.text == Cmd.NEWPAGE):
                elem = directives[Cmd.NEWPAGE]
            elif (elem.text == Cmd.TOC):
                if (doc.format == "docx"):
                    # para = [pf.Para(pf.Str("TABLE"), pf.Space(), pf.Str("OF"), pf.Space(), pf.Str("CONTENTS"))]
                    # div = pf.Div(*para, attributes={"custom-style": "TOC Header"})
                    elem = directives[Cmd.TOC]
                else:
                    elem = []
        return elem


def main(doc=None):
    dp = Docxtras()
    return pf.run_filter(dp.action, doc=doc)

if __name__ == "__main__":
    main()