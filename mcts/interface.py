import abc


class Clonable(abc.ABC):

    @abc.abstractmethod
    def clone(self) -> "Clonable":
        """
        Define method to deep clone self.
        """

    @abc.abstractmethod
    def __eq__(self, other) -> bool:
        """
        :returns: True if 'other' is the same
        """

