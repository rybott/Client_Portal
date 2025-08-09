from django.contrib import admin
from .models import LawFirm, LawFirmNote, Lawyer, LawyerNote,Company, CompanyNote, Case, CaseEvent, CaseNote, Task, TaskNote, DocumentReference

# Register all models here
admin.site.register(LawFirm)
admin.site.register(LawFirmNote)
admin.site.register(Lawyer)
admin.site.register(LawyerNote)
admin.site.register(Company)
admin.site.register(CompanyNote)
admin.site.register(Case)
admin.site.register(CaseEvent)
admin.site.register(CaseNote)
admin.site.register(Task)
admin.site.register(TaskNote)
admin.site.register(DocumentReference)