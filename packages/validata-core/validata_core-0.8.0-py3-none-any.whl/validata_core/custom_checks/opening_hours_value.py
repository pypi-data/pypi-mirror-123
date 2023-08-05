import opening_hours
from frictionless import Check, errors


class OpeningHoursValueError(errors.CellError):
    """Custom error."""

    code = "opening-hours-value"
    name = "Horaires d'ouverture incorrects"
    tags = ["#body"]
    template = (
        "La valeur '{cell}' n'est pas une définition d'horaire d'ouverture correcte."
    )
    description = (
        "L'expression d'horaires d'ouverture doit respecter la spécification"
        " [OpenStreetMap](https://wiki.openstreetmap.org/wiki/Key:opening_hours)."
    )


class OpeningHoursValue(Check):
    """Check opening hours validity."""

    possible_Errors = [OpeningHoursValueError]  # type: ignore

    def __init__(self, descriptor=None):
        super().__init__(descriptor)
        self.__column = self.get("column")

    def validate_start(self):
        if self.__column not in self.resource.schema.field_names:
            note = f"La colonne {self.__column!r} est manquante."
            yield errors.TaskError(note=note)

    def validate_row(self, row):
        cell_value = row[self.__column]

        # Empty cell, don't check!
        if not cell_value:
            return

        if not opening_hours.validate(cell_value):
            yield OpeningHoursValueError.from_row(
                row, note="", field_name=self.__column
            )

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["column"],
        "properties": {"column": {"type": "string"}},
    }
