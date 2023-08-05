# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Definition of Variable classes used for the WebApp model
"""
import base64
from django.db import models
from autoreduce_db.reduction_viewer.models import Instrument, ReductionRun


class Variable(models.Model):
    """
    Generic model class that should be treated as abstract
    """
    name = models.CharField(max_length=50, blank=False)
    value = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=50, blank=False)
    is_advanced = models.BooleanField(default=False)
    help_text = models.TextField(blank=True, null=True, default='')

    def encode_name_b64(self):
        """
        Encodes the name in a urlsafe base64 representaiton.
        Used to encode variable names with any character without
        special handling for having whitespaces or special characters.
        """
        # pylint:disable=no-member
        return base64.urlsafe_b64encode(self.name.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decode_name_b64(b64_encoded_name: str):
        """
        Decodes the base64 representation back to utf-8 string.
        """
        return base64.urlsafe_b64decode(b64_encoded_name).decode("utf-8")


class InstrumentVariable(Variable):
    """
    Instrument specific variable class

    - Holds the IDs of the variables used for the instrument

    - Holds `start_run` for functionality to "Configure new runs" - e.g. variables starting from `start_run` will
      use the defaults that are queried with

    """
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    experiment_reference = models.IntegerField(blank=True, null=True)
    start_run = models.IntegerField(blank=True, null=True)
    tracks_script = models.BooleanField(default=False)

    # pylint:disable=no-member
    def __str__(self):
        return f"{self.instrument.name} - {self.name}={self.value}"


class RunVariable(models.Model):
    """
    Run specific Variable class
    """
    variable = models.ForeignKey(Variable, related_name="runs", on_delete=models.CASCADE)
    reduction_run = models.ForeignKey(ReductionRun, related_name="run_variables", on_delete=models.CASCADE)
