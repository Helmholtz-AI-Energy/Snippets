import torch

from math import inf


class EarlyStopping:
    """
    This class implements Early Stopping for pytorch modules

    It is initialized with patience, which specifies after how many
    consecutive epochs worse than the best one stopping occurs.

    Given an instance called early_stopping, it should be used at the
    end of the training loop like this:

    if early_stopping(validation_loss, model):
        self.model.load_state_dict(early_stopping.best_state_dict)
        break

    The best loss can then be accessed with early_stopping.best_loss
    """
    def __init__(self, patience: int = 7):
        self._patience = patience
        self._patience_counter = 0
        self.best_loss = inf
        self.best_state_dict = None

    def __call__(self, loss: float, model: torch.nn.Module) -> bool:
        if loss < self.best_loss:
            self.best_loss = loss
            self.best_state_dict = model.state_dict()
            self._patience_counter = 0
            return False
        else:
            self._patience_counter += 1
            if self._patience_counter >= self._patience:
                return True
            else:
                return False
