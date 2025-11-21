from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional, List, Dict, Any

# Schedule Schemas
class ScheduleBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    slot_duration: int = 50

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_active: Optional[bool] = None

class Schedule(ScheduleBase):
    id: int
    psychologist_id: int
    is_active: bool
    exceptions: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Notification Schemas
class NotificationBase(BaseModel):
    title: str
    message: str
    type: str
    action_url: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    id: int
    user_id: int
    read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chat Schemas
class ChatMessageCreate(BaseModel):
    message: str
    context: Optional[str] = None

class ChatMessage(BaseModel):
    id: int
    user_id: int
    role: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Report Schemas
class ReportGenerate(BaseModel):
    type: str
    patient_id: Optional[int] = None
    start_date: date
    end_date: date
    include_charts: bool = True

class ReportData(BaseModel):
    id: int
    psychologist_id: int
    patient_id: Optional[int]
    type: str
    title: str
    content: str
    data: Dict[str, Any]
    start_date: Optional[date]
    end_date: Optional[date]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_patients: int
    active_patients: int
    total_sessions: int
    upcoming_sessions: int
    completed_this_month: int
    canceled_this_month: int
    attendance_rate: float

class DashboardPsychologist(BaseModel):
    statistics: DashboardStats
    upcoming_appointments: List[Any]
    recent_patients: List[Any]
    alerts: List[Dict[str, Any]]

class DashboardPatient(BaseModel):
    statistics: Dict[str, Any]
    upcoming_appointments: List[Any]
    psychologist: Optional[Any]

# Analytics Schemas
class AnalyticsOverview(BaseModel):
    total_sessions: int
    total_patients: int
    average_sessions_per_patient: float
    sessions_by_status: List[Dict[str, Any]]
    sessions_by_month: List[Dict[str, Any]]
    patients_by_risk_level: List[Dict[str, Any]]
    top_cancellation_reasons: List[Dict[str, Any]]

class AnalyticsTrends(BaseModel):
    data: List[Dict[str, Any]]
    trend: str
    change_percentage: float

# Search Schemas
class SearchResults(BaseModel):
    patients: List[Any]
    appointments: List[Any]
    total: int

# Available Slots Schema
class TimeSlot(BaseModel):
    time: str
    available: bool

class AvailableSlots(BaseModel):
    date: date
    slots: List[TimeSlot]