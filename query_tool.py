from pathlib import Path
from typing import Optional, Type, Any
from pydantic import BaseModel, Field, Extra
from langchain_core.tools import BaseTool
import sqlite3
import logging

# Anfrage, die Nutzende stellen
class QueryToolInput(BaseModel):
    query: str = Field(
        ...,
        description="sql_query",
    )


# Werkzeug (Tool), um die Datenbank abzufragen
class QueryTool(BaseTool):
    name: str = "studiengangstabelle_abfragen"
    description: str = "Gibt passende Studiengangsinfos für eine filterbasiere SQL-Abfrage zurück."
    args_schema: Type[BaseModel] = QueryToolInput

    class Config:
        extra = Extra.allow

    def __init__(self):
        """Initialisiere das Tool und lade die Vektordatenbank"""
        super().__init__()
        #self.conn = sqlite3.connect("beratung.db")

    def _run(self, query: str, **kwargs) -> Any:
        print(query)
        try:
            conn = sqlite3.connect("beratung.db")
            cursor = conn.cursor()
            cursor.execute(
                query.strip()
            )
            infos = cursor.fetchall()
            print(infos)
            #self.conn.close()
            return infos
        except Exception as e:
            return f"Error querying db: {str(e)}"
