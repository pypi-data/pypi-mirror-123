# -*- coding: utf-8 -*-
"""Control parameters for generating a structure from SMILES
"""

import logging
import seamm

logger = logging.getLogger(__name__)


class FromSMILESParameters(seamm.Parameters):
    """The control parameters for creating a structure from SMILES"""

    parameters = {
        "smiles string": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "s",
            "description": "SMILES:",
            "help_text": ("The SMILES string for the structure."),
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={
                **FromSMILESParameters.parameters,
                **seamm.standard_parameters.structure_handling_parameters,
                **defaults,
            },
            data=data,
        )
