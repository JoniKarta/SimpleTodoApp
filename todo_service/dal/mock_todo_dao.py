from typing import List

from todo_service.entities.mock_todo_entity import MockTodoEntity
from todo_service.enums.todo_priority import Priority

todos: List[MockTodoEntity] = [
    MockTodoEntity(title="Complete project report", description="Finish the quarterly project report", status="Pending",
               due_date="2024-12-05", priority=Priority.HIGH),
    MockTodoEntity(title="Buy groceries", description="Milk, eggs, bread, butter, and vegetables", status="In Progress",
               due_date="2024-11-25", priority=Priority.MEDIUM),
    MockTodoEntity(title="Call plumber", description="Fix the leaking sink in the kitchen", status="Pending",
               due_date="2024-11-30", priority=Priority.HIGH),
    MockTodoEntity(title="Renew gym membership", description="Renew membership for the upcoming year", status="Completed",
               due_date="2024-11-15", priority=Priority.LOW),
    MockTodoEntity(title="Doctor's appointment", description="Annual checkup with Dr. Smith", status="Pending",
               due_date="2024-12-01", priority=Priority.MEDIUM),
    MockTodoEntity(title="Clean the house", description="General house cleaning and organizing", status="In Progress",
               due_date="2024-11-27", priority=Priority.LOW),
    MockTodoEntity(title="Prepare presentation", description="Prepare slides for the company meeting", status="Pending",
               due_date="2024-12-10", priority=Priority.HIGH),
    MockTodoEntity(title="Pay electricity bill", description="Pay the monthly electricity bill before due date",
               status="Completed", due_date="2024-11-20", priority=Priority.MEDIUM),
    MockTodoEntity(title="Order birthday gift", description="Buy a gift for Sarah's birthday", status="Pending",
               due_date="2024-12-02", priority=Priority.LOW),
    MockTodoEntity(title="Submit assignment", description="Complete and submit the university assignment",
               status="Pending", due_date="2024-11-28", priority=Priority.HIGH)
]


def get_todo_dao():
    return todos
