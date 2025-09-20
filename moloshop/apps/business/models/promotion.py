#
# # apps/business/models/promotion.py
#
# from django.db import models
# from apps.core.models.abstract import SlugNamespaceModel
# from .business import Business
#
# class Promotion(SlugNamespaceModel):
#     business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="promotions")
#     description = models.TextField(blank=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     is_active = models.BooleanField(default=True)
#
#     class Meta:
#         verbose_name = "Акция"
#         verbose_name_plural = "Акции"
#
#     def save(self, *args, **kwargs):
#         if not self.namespace and self.business_id:
#             self.namespace = str(self.business_id)
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.title} ({self.business})"
