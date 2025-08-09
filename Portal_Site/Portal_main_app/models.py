from django.db import models


# ============================
# Law Firms and Lawyers
# ============================

class LawFirm(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LawFirmNote(models.Model):
    law_firm = models.ForeignKey(LawFirm, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Lawyer(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    law_firm = models.ForeignKey(LawFirm, on_delete=models.SET_NULL, null=True, related_name='lawyers')
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True) 
    phone_number = models.CharField(max_length=20, blank=True, null=True) 


    def __str__(self):
        return self.name


class LawyerNote(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ============================
# Companies (Plaintiff / Defendant)
# ============================

class Company(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CompanyNote(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ============================
# Cases
# ============================

class Case(models.Model):
    CASE_TYPES = [
        ('civil', 'Civil'),
        ('litigation', 'Litigation'),
        ('tax', 'Tax'),
        ('Accounting', 'Accounting'),
        ('Chapter7', "chapter7"),
        ('Chapter11', "chapter11"),
        ('Chapter13', "chapter13"),
        ('other', 'Other'),
        ('Monitorship', 'Monitorship'),
        ('Receivership', 'Receivership'),
    ]

    last_worked_on = models.DateField(null=True, blank=True)

    STAGE_CHOICES = [
        ('initial', 'Initial Intake'),
        ('discovery', 'Discovery'),
        ('analysis', 'Analysis'),
        ('trial', 'Trial Preparation'),
        ('closed', 'Closed'),
    ]
    Hired_by_choice = [
        ('plantiff', 'Plaintiff'),
        ('defendant','Defendant'),
        ('other','Other')
    ]
    summary = models.TextField(blank=True, null=True)
    short_name = models.CharField(max_length=100, unique=True)
    case_number = models.CharField(max_length=100, unique=True)
    case_type = models.CharField(max_length=50, choices=CASE_TYPES)
    hired_by = models.CharField(max_length=50, choices=Hired_by_choice, default='Other')
    date_of_case = models.DateField()
    plaintiff = models.CharField(max_length=255)
    defendant = models.CharField(max_length=255)
    plaintiff_lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, related_name='plaintiff_cases')
    defense_lawyer = models.ForeignKey(Lawyer, on_delete=models.SET_NULL, null=True, related_name='defense_cases')
    status = models.CharField(max_length=50, default='Open')
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, default='initial')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_number} ({self.case_type})"

class CaseEvent(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=255)  # e.g., “Filed”, “Report Due”
    event_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']  # optional

    def __str__(self):
        return f"{self.case.case_number} - {self.event_name} on {self.event_date}"

class CaseNote(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ============================
# Tasks
# ============================

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('waiting_docs', 'Waiting for Documents'),
        ('waiting_next', 'Waiting for Next Steps'),
        ('complete', 'Complete'),
    ]

    task_type = models.CharField(max_length=255)
    summary = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_type} ({self.case.case_number})"


class TaskNote(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ============================
# Document References (Metadata Only)
# ============================

class DocumentReference(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('bank_stmt', 'Bank Statement'),
        ('check', 'Check'),
        ('invoice', 'Invoice'),
        ('excel', 'Excel Table'),
        ('other', 'Other'),
    ]

    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255, help_text="e.g., Client, Subpoena, Discovery", blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, related_name='documents')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name='documents')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.document_type}"

