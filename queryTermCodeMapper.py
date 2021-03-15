from UiDataModel import del_keys, del_none, TerminologyEntry, TermCode
import json


def to_term_code_node(category_entries):
    root = TermCodeNode(TermCode("", "", ""))
    for entry in category_entries:
        root.children.append(TermCodeNode(entry))
    return root


class TermCodeNode:
    DO_NOT_SERIALIZE = ["DO_NOT_SERIALIZE"]

    def __init__(self, *args):
        if isinstance(args[0], TerminologyEntry):
            terminology_entry = args[0]
            self.termCode = terminology_entry.termCode if terminology_entry.termCode else None
            self.children = self.get_term_codes(terminology_entry)
        elif isinstance(args[0], TermCode):
            self.termCode = args[0]
            self.children = []

    @staticmethod
    def get_term_codes(terminology_entry: TerminologyEntry):
        result = []
        for child in terminology_entry.children:
            for valueDefinition in child.valueDefinitions:
                for selectableConcept in valueDefinition.selectableConcepts:
                    result.append(TermCodeNode(selectableConcept))
            result.append(TermCodeNode(child))
        return result

    def to_json(self):
        return json.dumps(self, default=lambda o: del_none(
            del_keys(o.__dict__, self.DO_NOT_SERIALIZE)), sort_keys=True, indent=4)