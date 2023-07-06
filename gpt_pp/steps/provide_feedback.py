from ..system import System
from ..ui import UI


def provide_feedback(system: System):
    """Prompt the user to provide feedback on the work the
    application has done. Add the response to chat memory.
    """
    feedback = UI.prompt("Provide feedback on the work done so far")
    system.memory.add_user_message(feedback)
