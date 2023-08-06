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

from typing import Sequence

import matplotlib.pyplot as pypl
import numpy as nmpy
import scipy.interpolate as ntrp
import skimage.measure as msre
from matplotlib.backend_bases import MouseEvent as mouse_event_t
from matplotlib.text import Annotation as annotation_t
from matplotlib.widgets import Slider as slider_t
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t

from cell_tracking_BC.in_out.file.archiver import archiver_t


array_t = nmpy.ndarray


def ShowFramesAs2DpT(
    segmentations: Sequence[array_t],
    with_labels: bool,
    figure: pypl.Figure,
    axes: pypl.Axes,
    /,
) -> slider_t:
    """
    Returns the slider so that a reference can be kept in calling function to maintain it responsive
    """
    _ShowFrame(segmentations[0], with_labels, axes)

    figure.subplots_adjust(bottom=0.25)
    slider_axes = figure.add_axes([0.25, 0.15, 0.65, 0.03])
    slider = slider_t(
        slider_axes,
        "Time Point",
        0,
        segmentations.__len__() - 1,
        valinit=0,
        valstep=1,
    )

    def OnNewSliderValue(value: float, /) -> None:
        time_point = int(round(value))
        _ShowFrame(segmentations[time_point], with_labels, axes)
        figure.canvas.draw_idle()

    def OnScrollEvent(event: mouse_event_t) -> None:
        new_value = slider.val + nmpy.sign(event.step)
        new_value = min(max(new_value, slider.valmin), slider.valmax)
        slider.set_val(new_value)

    slider.on_changed(OnNewSliderValue)
    figure.canvas.mpl_connect("scroll_event", OnScrollEvent)

    return slider


def ShowFramesAsMilleFeuille(
    segmentations: Sequence[array_t],
    with_labels: bool,
    axes: axes_3d_t,
    /,
    *,
    n_levels: int = 1,
) -> None:
    """"""
    n_segmentations = segmentations.__len__()
    shape = segmentations[0].shape

    all_rows, all_cols = nmpy.meshgrid(range(shape[0]), range(shape[1]), indexing="ij")
    for t_idx, segmentation in enumerate(segmentations):
        axes.contourf(
            all_rows,
            all_cols,
            segmentation,
            levels=n_levels,
            offset=t_idx,
            alpha=0.8,
            cmap="gray",
        )
        if with_labels:
            _AnnotateCells(segmentation, axes, elevation=t_idx + 0.2)
    SetZAxisProperties(n_segmentations - 1, axes)


def ShowFramesAsTunnels(
    segmentations: Sequence[array_t],
    axes: axes_3d_t,
    /,
    *,
    iso_value: float = 0.5,
) -> None:
    """"""
    n_segmentations = segmentations.__len__()
    volume = nmpy.array(segmentations, dtype=nmpy.uint8)
    original_extents = (
        range(n_segmentations),
        range(volume.shape[1]),
        range(volume.shape[2]),
    )
    interpolated_extents = (
        nmpy.linspace(0, n_segmentations - 1, num=n_segmentations),
        *original_extents[1:],
    )
    all_times, all_rows, all_cols = nmpy.meshgrid(*interpolated_extents, indexing="ij")
    interpolated_sites = nmpy.vstack((all_times.flat, all_rows.flat, all_cols.flat)).T
    interpolated = ntrp.interpn(original_extents, volume, interpolated_sites)
    reshaped = nmpy.reshape(
        interpolated, (interpolated_extents[0].size, *volume.shape[1:])
    )
    reorganized = nmpy.moveaxis(reshaped, (0, 1, 2), (2, 0, 1))
    flipped = nmpy.flip(reorganized, axis=2)
    vertices, faces, *_ = msre.marching_cubes(flipped, iso_value, step_size=5)
    axes.plot_trisurf(
        vertices[:, 0],
        vertices[:, 1],
        faces,
        nmpy.amax(vertices[:, 2]) - vertices[:, 2],
        cmap="rainbow",
        lw=1,
    )
    SetZAxisProperties(n_segmentations - 1, axes)


def _ShowFrame(segmentation: array_t, with_labels: bool, axes: pypl.Axes, /) -> None:
    """"""
    axes.matshow(segmentation, cmap="gray")
    if with_labels:
        _AnnotateCells(segmentation, axes)


def _AnnotateCells(
    segmentation: array_t, axes: pypl.Axes, /, *, elevation: float = None
) -> None:
    """"""
    if elevation is None:
        AnnotateCell = lambda _pos, _txt: axes.annotate(
            _txt,
            _pos,
            ha="center",
            fontsize="x-small",
            color="red",
        )

        annotations = (
            _chd for _chd in axes.get_children() if isinstance(_chd, annotation_t)
        )
        for annotation in annotations:
            annotation.remove()
    else:
        AnnotateCell = lambda _pos, _txt: axes.text(
            *_pos, _txt, fontsize="x-small", color="red"
        )

    labeled = msre.label(segmentation, connectivity=1)
    cells_properties = msre.regionprops(labeled)
    for properties in cells_properties:
        if elevation is None:
            position = nmpy.flipud(properties.centroid)
        else:
            position = (*properties.centroid, elevation)
        AnnotateCell(position, str(properties.label))


def SetTimeAxisProperties(highest_value: int, axes: pypl.Axes, /) -> None:
    """"""
    axes.set_xlim(0, highest_value)
    axes.set_xticks(range(highest_value + 1))
    axes.set_xticklabels(str(_idx) for _idx in range(highest_value + 1))


def SetZAxisProperties(z_max: int, axes: axes_3d_t, /) -> None:
    """"""
    axes.set_zlim(0, z_max)

    n_ticks = min(20, z_max + 1)
    axes.set_zticks(nmpy.linspace(0.0, z_max, num=n_ticks))
    axes.set_zticklabels(
        str(round(z_max * _idx / (n_ticks - 1), 1)) for _idx in range(n_ticks)
    )


def FinalizeDisplay(
    figure: pypl.Figure, figure_name: str, show_and_wait: bool, archiver: archiver_t, /
) -> None:
    """"""
    if archiver is not None:
        figure.canvas.draw_idle()
        archiver.Store(figure, figure_name)

    if show_and_wait:
        pypl.show()
