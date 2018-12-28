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

        Precondition:
        ----------
        The tasks for this task are not done (i.e. a call
        to is_done() should return false before this method is
        called)

        Postcondition:
        ----------
        If the tasks for this task were completed during this
        iteration, calls to is_done will return true

        Returns:
        ----------
        None
        """
        pass

    @abc.abstractmethod
    def is_done(self):
        """
        Returns true if the tasks for this task have been 
        completed, and false otherwise.

        Parameters
        ----------
        None

        Precondition:
        ----------
        None

        Postcondition:
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
        event's response is set (wait_r()).

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
        TwoWayEvent
        """
        pass