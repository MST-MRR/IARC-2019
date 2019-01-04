# Standard Library
import abc

class InstructionBase():
    """
    Responsible for decoding data sent over the network and
    using that data to create tasks.

    NOTE: This class will be import once we start sending
    messages over the network, but is currently in a simplified
    state.
    """
    __metaclass__ = abc.ABCMeta

    # Subclasses of this class should define an init function

    @abc.abstractmethod
    def get_task(self):
        """
        Decodes the raw instruction data into the appropriate instance
        of a Task object, which should be fully configured and ready
        for the do() function to be called.

        Parameters
        ----------
        None
        
        Precondition:
        ----------
        The instruction has been properly initialized (given the appropriate
        raw data for this kind of instruction class).

        Postcondition:
        ----------
        None

        Returns:
        ----------
        Task object of the appropriate type
        """
        pass
