# Standard Library
import abc

class TaskBase():
    """
    Responsible for implementing the core logic of the various actions
    that a drone can take (ex. Movement, Follow, Heal, Decode). Must, at
    a minimum, implement do(), is_done(), and exit_task().
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def do(self):
        """
        Does one iteration of the logic for this task

        Parameters
        ----------
        None (maybe kwargs in the future?)

        Returns:
        ----------
        True if the task is done with its goal, and false otherwise
        (But do not use to query if the task is done, use is_done() instead)
        """
        pass

    @abc.abstractmethod
    def is_done(self):
        """
        Returns true if the task is done doing
        whatever is does, and false otherwise.

        Parameters
        ----------
        None

        Returns:
        ----------
        Boolean
        """
        pass

    @abc.abstractmethod
    def exit_task(self):
        """
        Takes the necessary actions to for the controller to
        safely exit the current task (ex. halting movement). 
        The task has been safely exited once the returned 
        event is set.

        Parameters
        ----------
        None

        Precondition:
        ----------
        None

        Postcondition:
        ----------
        The current task can be discarded

        Returns:
        ----------
        threading.Event
        """
        pass