# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2019 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""Models that represent the tables in the database."""
# pylint:disable=no-member
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db import models


class Instrument(models.Model):
    """Holds data about an Instrument."""
    name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    is_flat_output = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_last_for_rerun(self, runs=None):
        """
        Return the last non-skipped run. If all the runs are skipped, return the
        last skipped run.
        """
        if not runs:
            runs = self.reduction_runs.all()

        last_run = runs.exclude(status=Status.get_skipped()).last()
        if not last_run:
            last_run = runs.last()

        return last_run


class Experiment(models.Model):
    """Holds data about an Experiment."""
    reference_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"RB{self.reference_number}"


class Status(models.Model):
    """Enum table for status types of messages."""
    _cached_statuses = {}
    STATUS_CHOICES = (('q', 'Queued'), ('p', 'Processing'), ('s', 'Skipped'), ('c', 'Completed'), ('e', 'Error'))

    value = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def value_verbose(self):
        """Return the status as its textual value."""
        return dict(Status.STATUS_CHOICES)[self.value]

    def __str__(self) -> str:
        return self.value_verbose()

    @staticmethod
    def _get_status(status_value: str):
        """
        Return a status matching the given name or create one if it doesn't yet
        exist.

        Args:
            status_value: The value of the status record in the database.
        """
        if status_value in Status._cached_statuses:
            return Status._cached_statuses[status_value]
        else:
            status_record = Status.objects.get_or_create(value=status_value)[0]
            Status._cached_statuses[status_value] = status_record

        return status_record

    @staticmethod
    def get_error():
        """Return the error status."""
        return Status._get_status('e')

    @staticmethod
    def get_completed():
        """Return the completed status."""
        return Status._get_status('c')

    @staticmethod
    def get_processing():
        """Return the processing status."""
        return Status._get_status('p')

    @staticmethod
    def get_queued():
        """Return the queued status."""
        return Status._get_status('q')

    @staticmethod
    def get_skipped():
        """Return the skipped status."""
        return Status._get_status('s')


class Software(models.Model):
    """Represents the software used to perform the reduction."""
    name = models.CharField(max_length=100, blank=False, null=False)
    version = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return f"{self.name}-{self.version}"


class ReductionRun(models.Model):
    """
    Table designed to link all table together. This represents a single
    reduction run that takes place at ISIS. Thus, this will store all the
    relevant data regarding that run.
    """
    # Integer fields
    run_version = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    started_by = models.IntegerField(null=True, blank=True)

    # Char fields
    run_description = models.CharField(max_length=200, blank=True)
    run_title = models.CharField(max_length=200, blank=True)

    # Text fields
    admin_log = models.TextField(blank=True)
    graph = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    reduction_log = models.TextField(blank=True)
    reduction_host = models.TextField(default="", blank=True, verbose_name="Reduction hostname")
    # Scripts should be 100,000 chars or less. The DB supports up to 4GB strings here
    script = models.TextField(blank=False, validators=[MaxLengthValidator(100000)])

    # Date time fields
    created = models.DateTimeField(auto_now_add=True, blank=False)
    finished = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, blank=False)
    retry_when = models.DateTimeField(null=True, blank=True)
    started = models.DateTimeField(null=True, blank=True)

    # Bool field
    hidden_in_failviewer = models.BooleanField(default=False)
    overwrite = models.NullBooleanField(default=True)
    batch_run = models.BooleanField(default=False)

    # Foreign Keys
    experiment = models.ForeignKey(Experiment, blank=False, related_name='reduction_runs', on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, related_name='reduction_runs', null=True, on_delete=models.CASCADE)
    retry_run = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, blank=False, related_name='+', on_delete=models.CASCADE)
    # Allowed software field to be black in code line below. Issued opened (#852) to later
    # populate this field
    software = models.ForeignKey(
        Software,
        blank=True,
        related_name='reduction_runs',
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title()

    def title(self):
        """
        Return an interface-friendly name that identifies this run using either
        run name or run version.
        """
        try:
            title = f"{self.run_number}"
        except ValueError:
            title = f"Batch {self.run_numbers.first()} → {self.run_numbers.last()}"

        if self.run_version > 0:
            title += f" - {self.run_version}"

        if self.run_title:
            title += f" - {self.run_title}"

        return title

    @property
    def run_number(self) -> int:
        """
        Return the value of the run_number, if only a single one is associated
        with this run. This replicates the behaviour of a one to one
        relationship between a ReductionRun and a RunNumber.
        """
        if self.run_numbers.count() == 1:
            return self.run_numbers.first().run_number
        else:
            raise ValueError(
                "This run has more then one run_number associated with it. You must iterate run_numbers manually")


class RunNumber(models.Model):
    run_number = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    reduction_run = models.ForeignKey(ReductionRun, blank=False, related_name='run_numbers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.run_number}"


class DataLocation(models.Model):
    """Represents the location at which the unreduced data is stored on disk."""
    file_path = models.CharField(max_length=255)
    reduction_run = models.ForeignKey(ReductionRun, blank=False, related_name='data_location', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.file_path}"


class ReductionLocation(models.Model):
    """Represents the location at which the reduced data is stored on disk."""
    file_path = models.CharField(max_length=255)
    reduction_run = models.ForeignKey(
        ReductionRun,
        blank=False,
        related_name='reduction_location',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.file_path}"


class Setting(models.Model):
    """Represents additional settings options for the reduction run."""
    name = models.CharField(max_length=50, blank=False)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} = {self.value}"


class Notification(models.Model):
    """Represents possible notification messages regarding reduction runs."""
    SEVERITY_CHOICES = (('i', 'info'), ('w', 'warning'), ('e', 'error'))

    message = models.CharField(max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    severity = models.CharField(max_length=1, choices=SEVERITY_CHOICES, default='i')
    is_staff_only = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification: {self.message}"

    def severity_verbose(self):
        """Return the severity as its textual value."""
        return dict(Notification.SEVERITY_CHOICES)[self.severity]


class OutputType(models.Model):
    """
    Represents the output types of file that can be output from a job. This is
    an enum table.
    """
    type = models.CharField(max_length=50, blank=False)


class Output(models.Model):
    """Represents the output of a reduction job (file path and type)."""
    job = models.ForeignKey(ReductionRun, blank=False, related_name='output', on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255, blank=False)
    type = models.ForeignKey(OutputType, blank=False, related_name='output', on_delete=models.CASCADE)
