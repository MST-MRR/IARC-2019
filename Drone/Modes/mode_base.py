# Standard Library
import abc

class ModeBase():
    """
    Responsible for implementing the core logic of the various actions
    that a drone can take (ex. Movement, Follow, Heal, Decode). Must, at
    a minimum, implement do(), is_done(), and exit_mode().
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def do(self):
        """
        Does one iteration of the logic for this mode

        Parameters
        ----------
        None (maybe kwargs in the future?)

        Precondition:
        ----------
        The tasks for this mode are not done (i.e. a call
        to is_done() should return false before this method is
        called)

        Postcondition:
        ----------
        If the tasks for this mode were completed during this
        iteration, calls to is_done will return true

        Returns:
        ----------
        None
        """
        pass

    @abc.abstractmethod
    def is_done(self):
        """
        Returns true if the tasks for this mode have been 
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
    def exit_mode(self):
        """
        Takes the necessary actions to for the controller to
        safely exit the current mode (ex. halting movement). 
        The mode has been safely exited once the returned 
        event's response is set (wait_r()).

        Parameters
        ----------
        None

        Precondition:
        ----------
        None

        Postcondition:
        ----------
        The current mode can be discarded

        Returns:
        ----------
        TwoWayEvent
        """
        pass