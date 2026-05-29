from pathlib import Path
from typing import Optional, Type, Any
from pydantic import BaseModel, Field, Extra
from langchain_core.tools import BaseTool

# Anfrage, die Nutzende stellen
class InfoToolInput(BaseModel):
    query: str = Field(
        ...,
        description="studiengang",
    )


# Werkzeug (Tool), um die Datenbank abzufragen
class InfoTool(BaseTool):
    name: str = "studiengangsinfos_abfragen"
    description: str = "Gib die Studiengangsinfos für einen gegebenen Studiengang."
    args_schema: Type[BaseModel] = InfoToolInput

    class Config:
        extra = Extra.allow

    def __init__(self):
        """Initialisiere das Tool und lade die Vektordatenbank"""
        super().__init__()
        courses = {
            "AI Engineering": "ai-engineering.md",
            "Angewandte Chemie": "angewandte-chemie.md",
            "Angewandte Medien und Kulturwissenschaft": "angewandte-medien-und-kulturwissenschaft.md",
            "Angewandte Informatik": "angewandte-informatik.md",
            "Angewandte Sexualwissenschaft": "angewandte-sexualwissenschaft.md",
            "Automatisierungstechnik und Informatik": "automatisierungstechnik-und-informatik.md",
            "BWL": "bwl.md",
            "BWL (Berufsbegleitend)": "bwl-(berufsbegleitend).md",
            "Chemie- und Umwelttechnik": "chemie-und-umwelttechnik.md",
            "Controlling und Management": "controlling-und-management.md",
            "Elektrotechnik und Automatisierungstechnik": "elektrotechnik-und-automatisierungstechnik.md",
            "Engineering und Management": "engineering-und-management.md",
            "Green Engineering": "green-engineering.md",
            "Informationsdesign und Medien": "informationsdesign-und-mediendesign.md",
            "Ingenieurpädagogik": "ingenieuerpädagogik.md",
            "KMP":"kmp.md",
            "KOMPASS": "kompass.md",
            "Maschinenbau Bachelor": "maschinenbau-b.md",
            "Maschinenbau Master": "maschinenbau-m.md",
            "Nachhaltige Verfahrenstechnik und Chemie": "nachhaltige-verfahrenstechnik-und-chemie.md",
            "Polymer Material Science": "polymer-material-science.md",
            "Projektmanagement": "projektmanagement.md",
            "Sexologie": "sexologie.md",
            "Soziale Arbeit": "soziale-arbeit.md",
            "Systemische Soziale Arbeit": "systemische-soziale-arbeit.md",
            "Technisches Informationsdesign": "technisches-informationsdesign.md",
            "Wirtschaftsinformatik Bachelor": "wirtschaftsinformatik-b.md",
            "Wirtschaftsinformatik Master": "wirtschaftsinformatik-m.md",
            "Wirtschaftsingnieurwesen Dual": "wirtschaftsingnieurwesen_dual.md",
            "Wirtschaftsingenieurwesen": "wirtschaftsingenieurwesen.md"

        }
        self.courses = courses

    def _run(self, query: str, **kwargs) -> Any:
        try:
            if query.lower().endswith(".md"):
                path = Path("studiengaenge") / query
            else:
                path = Path("studiengaenge") / self.courses[query]
            with path.open("r", encoding="utf-8") as info_file:
                info = info_file.read()
                print(info)
            return info
        except Exception as e:
            print(e)
            return f"Error getting information: {str(e)}"
