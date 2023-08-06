import logging

logger = logging.getLogger(__name__)
from typing import List

import numpy as np
from scipy.special import erf

from . import SizeDistributionBaseModel as PSDBase


class LogNormal(PSDBase.SizeDistributionBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_par_str: List[str] = ["Dm", "delta"]
        self.model_expression_str: str = (
            "X(d) = 0.5*[1 + erf(Z)]; Z = ln(d/Dm) / [(sqrt(2) * ln(delta) ) ]"
        )

        self.model_name_str: str = "Log-normal"
        logger.info("{} object constructed".format(self.model_name_str))
        self.sqrt2: float = np.sqrt(2.0)

    def specificModel(
        self, d: PSDBase.ArrayOrFloat, *args: float
    ) -> PSDBase.ArrayOrFloat:
        D50 = args[0]
        delta = args[1]
        Z = np.log(d / D50) / (self.sqrt2 * np.log(delta))
        return np.array(0.5 * (1 + erf(Z)))

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        D50 = self.getDn(x, y, 0.5, 100)
        D84 = self.getDn(x, y, 0.84, 120)
        delta = D84 / D50
        return [D50, delta]

    def getSauterDiameterValue(self) -> float:
        D50 = self.model_par_values[0]
        delta = self.model_par_values[1]
        return float(D50 * np.exp(-0.5 * np.log(delta) ** 2))

    def getSauterDiameterExpression(self) -> str:
        return "dps = Dm*exp(-0.5 * ln(delta)^2)"
