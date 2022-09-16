from . import BaseClass


class Meta(BaseClass.Base):

    """
    Class which holds information about the piece.


    # Optional inputs
    # HKT: renamed 'title' to 'movement_title', added 'work_title', 'work_number' and 'movement_number'.
    - work_title: name of the work
    - work_number: name of the work
    - movement_title: name of the movement

    - composer

    - copyright: company or tag line who owns the copyright
    """

    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        # HKT: added work_title
        if "work_title" in kwargs:
            if kwargs["work_title"] is not None:
                self.work_title = kwargs["work_title"]
        # HKT: added work_number
        if "work_number" in kwargs:
            if kwargs["work_number"] is not None:
                self.work_number = kwargs["work_number"]
        # HKT: renamed title to movement_title
        if "movement_title" in kwargs:
            if kwargs["movement_title"] is not None:
                self.movement_title = kwargs["movement_title"]
        # HKT: added movement_number
        if "movement_number" in kwargs:
            if kwargs["movement_number"] is not None:
                self.movement_number = kwargs["movement_number"]
        if "composer" in kwargs:
            if kwargs["composer"] is not None:
                self.composer = kwargs["composer"]
        if "copyright" in kwargs:
            if kwargs["copyright"] is not None:
                self.copyright = kwargs["copyright"]

    def EscapeQuotes(self, value):
        list_of_string = list(value)
        output = []
        for item in list_of_string:
            if item == "\"":
                output.append("\\")
            output.append(item)
        return "".join(output)

    def toLily(self):
        val = "\header {\n"
        # HKT: FIXME replaced title with mxmxl work_title and movement_title so
        #  passing lilypond the movement_title to keep the original consistent
        if hasattr(self, "movement_title") and self.movement_title is not None:
            val += "title = \"" + self.EscapeQuotes(self.movement_title) + "\"\n"
        if hasattr(self, "composer") and self.composer is not None:
            val += "composer = \"" + self.EscapeQuotes(self.composer) + "\"\n"
        if hasattr(self, "copyright"):
            val += "tagline = \"" + self.EscapeQuotes(self.copyright) + "\""
        val += "\n}"
        if hasattr(self, "pageNum"):
            if self.pageNum:
                val += "\n \paper {\n print-page-number = True \n}\n\n"
        if hasattr(self, "credits"):
            val += "\\markuplist {"
            for credit in self.credits:
                val += "\n\\vspace #0.5\n"
                val += "\n" + credit.toLily()
            val += " }"

        return val

    def AddCredit(self, credit):
        if not hasattr(self, "credits"):
            self.credits = []
        self.credits.append(credit)
