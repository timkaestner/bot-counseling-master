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
            "Angewandte Chemie": "angewandte-chemie.md"
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
