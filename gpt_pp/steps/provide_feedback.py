from ..system import System
from ..ui import UI


def provide_feedback(system: System):
    feedback = UI.prompt("Provide feedback")
    system.memory.add_user_message(feedback)
