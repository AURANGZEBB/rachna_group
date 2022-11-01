from odoo import models, fields, api
import datetime
from datetime import date

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    status = fields.Selection(
        selection=[
            ('present', 'Present'),
            ('half_day', 'Half Day'),
            ('absent', 'Absent'),
            ('short_leave', 'Short Leave'),
            ('leave', 'Leave'),
        ],
        string='Status',
        default=''
    )
    day_status = fields.Float(string="Day Status")
    late_in = fields.Float(string="Late in")
    early_out = fields.Float(string="Early Out")
    shift_id = fields.Many2one("resource.calendar", string="Shift", related="employee_id.contract_id.resource_calendar_id")
    shift_check_in = fields.Float(string="Shift Check In", related="employee_id.contract_id.resource_calendar_id.attendance_ids.hour_from")
    shift_check_out = fields.Float(string="Shift Check Out", related="employee_id.contract_id.resource_calendar_id.attendance_ids.hour_to")
    standard_work_hours = fields.Float(string="Standard Hours", related="employee_id.contract_id.resource_calendar_id.hours_per_day")
    over_time = fields.Float(string="Overtime")

    def compute_attendance(self):
        for rec in self:
            actual_checkin = rec.check_in + datetime.timedelta(hours=5)
            datetime_actual_00 = datetime.datetime(actual_checkin.year, actual_checkin.month, actual_checkin.day)
            shift_checkin = datetime_actual_00 + datetime.timedelta(hours=rec.shift_check_in)
            shif_checkout = shift_checkin + datetime.timedelta(hours=rec.standard_work_hours)
            actual_checkout = rec.check_out + datetime.timedelta(hours=5)
            overtime = rec.worked_hours - rec.standard_work_hours if rec.worked_hours > rec.standard_work_hours else 0.0
            rec.over_time = overtime
            if actual_checkin > shift_checkin:
                allowed_minutes = 15.00
                actual_late_in_mins_delta = actual_checkin - shift_checkin
                actual_late_in_mins = actual_late_in_mins_delta.total_seconds() * 1/12
                print(float(actual_late_in_mins))
                if actual_late_in_mins > allowed_minutes:
                    rec.late_in = actual_late_in_mins
                else:
                    rec.late_in = 0.0
            if actual_checkout < shift_checkin:
                allowed_minutes = 15
                actual_early_out_mins_delta = shif_checkout - actual_checkout
                actual_early_out_mins = actual_early_out_mins_delta * 1/12
                if actual_early_out_mins > allowed_minutes:
                    rec.early_out = actual_early_out_mins
                else:
                    rec.early_out = 0.0