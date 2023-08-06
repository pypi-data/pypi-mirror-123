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

from __future__ import annotations

import dataclasses as dtcl
from typing import Callable, Dict, Sequence, Tuple, Union

import matplotlib.pyplot as pypl
import numpy as nmpy
import scipy.interpolate as ntrp
import skimage.measure as msre
from matplotlib.backend_bases import MouseEvent as mouse_event_t
from matplotlib.image import AxesImage as axes_image_t
from matplotlib.text import Annotation as annotation_t
from matplotlib.widgets import Slider as slider_t
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t

from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.type.frame import frame_t
from cell_tracking_BC.type.segmentation import compartment_t
from cell_tracking_BC.type.segmentations import segmentations_t
from cell_tracking_BC.type.sequence import sequence_t


array_t = nmpy.ndarray
sequence_h = Union[Sequence[array_t], segmentations_t, sequence_t]
all_versions_h = Dict[str, Union[Sequence[array_t], Sequence[frame_t]]]


@dtcl.dataclass(repr=False, eq=False)
class sequence_2D_t:

    figure: pypl.Figure
    axes: pypl.Axes
    frame: axes_image_t
    slider: slider_t

    all_versions: all_versions_h
    current_version: str = None
    with_labels: bool = True

    @classmethod
    def NewForChannels(
        cls,
        sequence: Union[Sequence[array_t], sequence_t],
        /,
        *,
        figure_name: str = "sequence",
        archiver: archiver_t = None,
    ) -> sequence_2D_t:
        """"""
        return cls._NewForSequence(
            sequence,
            _AllChannelsOfSequence,
            with_labels=False,
            figure_name=figure_name,
            archiver=archiver,
        )

    @classmethod
    def NewForSegmentation(
        cls,
        sequence: sequence_h,
        /,
        *,
        with_labels: bool = True,
        figure_name: str = "segmentation",
        archiver: archiver_t = None,
    ) -> sequence_2D_t:
        """"""
        return cls._NewForSequence(
            sequence,
            _AllSegmentationsOfSequence,
            with_labels=with_labels,
            figure_name=figure_name,
            archiver=archiver,
        )

    @classmethod
    def _NewForSequence(
        cls,
        sequence: sequence_h,
        AllVersionsOfSequence: Callable[[sequence_h], Tuple[all_versions_h, str]],
        /,
        *,
        with_labels: bool = True,
        figure_name: str = "sequence",
        archiver: archiver_t = None,
    ) -> sequence_2D_t:
        """"""
        figure = pypl.figure()
        axes = figure.subplots()

        all_versions, current_version = AllVersionsOfSequence(sequence)
        if more_than_one := (all_versions.__len__() > 1):
            axes.set_title(current_version)

        first_key = tuple(all_versions.keys())[0]
        first_version = all_versions[first_key]
        first_segmentation = first_version[0]
        frame = axes.matshow(first_segmentation, cmap="gray")
        if with_labels:
            _AnnotateCells(first_segmentation, axes)

        slider_axes = figure.add_axes([0.15, 0.04, 0.7, 0.03])
        slider = slider_t(
            slider_axes,
            "Time Point",
            0,
            first_version.__len__() - 1,
            valinit=0,
            valstep=1,
        )

        instance = cls(
            figure=figure,
            axes=axes,
            frame=frame,
            slider=slider,
            all_versions=all_versions,
            current_version=current_version,
            with_labels=with_labels,
        )

        if more_than_one:
            figure.canvas.mpl_connect("button_press_event", instance._OnButtonPress)
        figure.canvas.mpl_connect("scroll_event", instance._OnSliderScrollEvent)
        slider.on_changed(instance._ShowFrame)

        FinalizeDisplay(figure, figure_name, False, archiver)

        return instance

    def _OnButtonPress(
        self,
        event: mouse_event_t,
        /,
    ) -> None:
        """"""
        if event.inaxes is self.axes:
            self._ShowNextVersion()

    def _OnSliderScrollEvent(self, event: mouse_event_t) -> None:
        """"""
        value = self.slider.val
        new_value = round(value + nmpy.sign(event.step))
        new_value = min(max(new_value, self.slider.valmin), self.slider.valmax)
        if new_value != value:
            self.slider.set_val(new_value)

    def _ShowFrame(
        self,
        time_point: Union[int, float],
        /,
    ) -> None:
        """"""
        time_point = int(time_point)
        segmentation = self.all_versions[self.current_version][time_point]
        self.frame.set_array(segmentation)
        self.frame.set_clim(nmpy.amin(segmentation), nmpy.amax(segmentation))

        if self.with_labels:
            _AnnotateCells(segmentation, self.axes)

        self.figure.canvas.draw_idle()

    def _ShowNextVersion(self) -> None:
        """"""
        all_names = tuple(self.all_versions.keys())
        where = all_names.index(self.current_version)
        where = (where + 1) % all_names.__len__()
        self.current_version = all_names[where]

        self.axes.set_title(self.current_version)
        self._ShowFrame(self.slider.val)

    def ShowAndWait(self) -> None:
        """"""
        pypl.show()


def _AllChannelsOfSequence(
    sequence: Union[Sequence[array_t], sequence_t]
) -> Tuple[all_versions_h, str]:
    """"""
    if isinstance(sequence, sequence_t):
        all_channels = {
            _chl: sequence.Frames(channel=_chl) for _chl in sequence.channels
        }
        current_channel = sequence.channels[0]
    else:
        current_channel = "MAIN"
        all_channels = {current_channel: sequence}

    return all_channels, current_channel


def _AllSegmentationsOfSequence(sequence: sequence_h) -> Tuple[all_versions_h, str]:
    """"""
    if isinstance(sequence, (segmentations_t, sequence_t)):
        if isinstance(sequence, segmentations_t):
            segmentations = sequence
        else:
            segmentations = sequence.segmentations

        all_versions = {}
        compartments, versions = segmentations.available_versions
        for compartment in compartments:
            for version in versions:
                key = f"{compartment.name}:{version[0]}:{version[1]}"
                all_versions[key] = segmentations.CompartmentsWithVersion(
                    compartment, index=version[0], name=version[1]
                )
        current_version = f"{compartment_t.CELL.name}:{versions[0][0]}:{versions[0][1]}"
    else:
        current_version = "MAIN"
        all_versions = {current_version: sequence}

    return all_versions, current_version


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

        to_be_removed = filter(
            lambda _art: isinstance(_art, annotation_t), axes.get_children()
        )
        # tuple: to build a static list before iterative removal, just in case
        for annotation in tuple(to_be_removed):
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


def FigureAnd3DAxes() -> Tuple[pypl.Figure, axes_3d_t]:
    """"""
    figure = pypl.figure()
    axes = figure.add_subplot(projection=axes_3d_t.name)
    axes.set_xlabel("row positions")
    axes.set_ylabel("column positions")
    axes.set_zlabel("time points")

    return figure, axes


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
