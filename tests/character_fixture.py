"""Historical data for testing gate mechanics ONLY, never production character approval.

The real study-02 design is rejected. These isolated fixtures let unit tests exercise
successful serialization paths without treating that design as aesthetically valid.
"""
import json
from unittest.mock import patch
from studio.character_art import MODEL


def mechanical_character_fixture():
    entry = json.loads(MODEL.read_text(encoding='utf-8'))['layers'][0]
    entry['character_qc']['status'] = 'passed'
    entry['character_qc']['scope'] = 'UNIT TEST ONLY: mechanics, not artistic approval'
    return entry


class MechanicalCharacterFixtureMixin:
    def setUp(self):
        super().setUp()
        for target, kwargs in (
            ('studio.character_qc.rejected_characters', {'return_value': []}),
            ('studio.character_art.reviewed_person', {'side_effect': mechanical_character_fixture}),
        ):
            context = patch(target, **kwargs); context.start(); self.addCleanup(context.stop)
