
# apps/business/utils/master_time.py

from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

def is_staff_available_for_service(staff, appointment_datetime, service_duration_minutes):
    """
    Проверяет доступность мастера staff в момент appointment_datetime
    с учетом рабочего расписания (WorkSchedule), перерывов (BreakTime),
    длительности услуги (service_duration_minutes) и текущих записей (OrderItem).
    """
    appointment_datetime = timezone.localtime(appointment_datetime)
    weekday = appointment_datetime.weekday()
    appointment_start_time = appointment_datetime.time()
    appointment_end_time = (appointment_datetime + timedelta(minutes=service_duration_minutes)).time()

    # Получение рабочих периодов мастера в день недели
    work_periods = staff.work_schedules.filter(weekday=weekday)
    if not work_periods.exists():
        raise ValidationError("Мастер не работает в выбранный день недели")

    for period in work_periods:
        # Проверяем, помещается ли запись во время рабочего периода
        if not (period.start_time <= appointment_start_time and appointment_end_time <= period.end_time):
            continue

        # Проверяем нет ли пересечения с перерывами
        conflict = False
        for br in period.breaks.all():
            if (appointment_start_time < br.break_end) and (appointment_end_time > br.break_start):
                conflict = True
                break
        if conflict:
            continue

        # Проверяем, не занято ли время другим заказом у данного мастера
        overlapping = staff.orderitem_set.filter(
            appointment_datetime__date=appointment_datetime.date()
        ).exclude(order__status='cancelled').filter(
            appointment_datetime__lt=appointment_datetime + timedelta(minutes=service_duration_minutes),
            appointment_datetime__gte=appointment_datetime
        )
        if overlapping.exists():
            continue

        # Все проверки пройдены - время доступно
        return True

    raise ValidationError("Мастер занят или недоступен в это время")
