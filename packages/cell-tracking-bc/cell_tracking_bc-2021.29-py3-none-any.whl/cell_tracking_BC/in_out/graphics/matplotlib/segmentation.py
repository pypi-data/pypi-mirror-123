# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Sequence, Union

import matplotlib.pyplot as pypl
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t
from numpy import ndarray as array_t

from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.in_out.graphics.matplotlib.generic import (
    FinalizeDisplay,
    ShowFramesAs2DpT,
    ShowFramesAsMilleFeuille,
    ShowFramesAsTunnels,
)
from cell_tracking_BC.type.sequence import sequence_t


def ShowSegmentation(
    sequence: Union[sequence_t, Sequence[array_t]],
    /,
    *,
    which_compartment: str = None,
    with_labels: bool = True,
    mode: str = "2d+t",
    show_and_wait: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> None:
    """
    which_compartment: "nucleus" or "cytoplasm" or "cell" or None. If None, then the first non-None in the order "cell",
    "cytoplasm", "nucleus" is selected.
    mode: see ShowSequence
    """
    if isinstance(sequence, sequence_t):
        if which_compartment == "nucleus":
            segmentations = sequence.nuclei_sgms
        elif which_compartment == "cytoplasm":
            segmentations = sequence.cytoplasms_sgms
        elif which_compartment == "cell":
            segmentations = sequence.cells_sgms
        elif which_compartment is None:
            if sequence.cells_sgms is not None:
                segmentations = sequence.cells_sgms
            elif sequence.cytoplasms_sgms is not None:
                segmentations = sequence.cytoplasms_sgms
            elif sequence.nuclei_sgms is not None:
                segmentations = sequence.nuclei_sgms
            else:
                raise RuntimeError("No segmentations computed yet")
        else:
            raise ValueError(f"{which_compartment}: Invalid compartment designation")
    else:
        segmentations = sequence

    figure = pypl.figure()

    if mode == "2d+t":
        axes = figure.add_subplot(111)
        # Maintain a reference to the slider so that it remains functional
        figure.__SEQUENCE_SLIDER_REFERENCE__ = ShowFramesAs2DpT(
            segmentations, with_labels, figure, axes
        )
    elif mode in ("mille-feuille", "tunnels"):
        axes = figure.add_subplot(projection=axes_3d_t.name)
        axes.set_xlabel("row positions")
        axes.set_ylabel("column positions")
        axes.set_zlabel("time points")

        if mode == "mille-feuille":
            ShowFramesAsMilleFeuille(segmentations, with_labels, axes)
        else:
            ShowFramesAsTunnels(segmentations, axes)
    else:
        raise ValueError(
            f'{mode}: Invalid mode; Expected="2d+t", "mille-feuille", "tunnels"'
        )

    FinalizeDisplay(figure, figure_name, show_and_wait, archiver)
