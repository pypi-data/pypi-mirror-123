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

from sys import maxsize as MAX_INTEGER
from typing import Dict, List, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as pypl
import networkx as grph
import numpy as nmpy
from matplotlib import cm as colormap_t
from matplotlib.backend_bases import MouseEvent as mouse_event_t
from matplotlib.collections import PathCollection as path_collection_t
from matplotlib.image import AxesImage as axes_image_t
from matplotlib.text import Annotation as annotation_t
from mpl_colors import Css4Color as CSS4COLORS
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t

from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.in_out.graphics.matplotlib.generic import FinalizeDisplay
from cell_tracking_BC.type.frame import frame_t
from cell_tracking_BC.type.sequence import sequence_t
from cell_tracking_BC.type.track import forking_track_t, single_track_t
import dataclasses as dtcl


array_t = nmpy.ndarray


@dtcl.dataclass(repr=False, eq=False)
class tracking_2D_t:

    figure: pypl.Figure
    axes_track: pypl.Axes
    axes_frame: pypl.Axes
    colormap: colormap_t

    scatter: path_collection_t = dtcl.field(init=False, default=None)
    annotation: annotation_t = dtcl.field(init=False, default=None)
    frame: axes_image_t = dtcl.field(init=False, default=None)

    all_versions: Dict[str, Union[Sequence[array_t], Sequence[frame_t]]]
    # Cell details
    labels: List[int] = dtcl.field(init=False, default_factory=list)
    time_points: List[int] = dtcl.field(init=False, default_factory=list)
    affinities: List[float] = dtcl.field(init=False, default_factory=list)
    colors: List[int] = dtcl.field(init=False, default_factory=list)

    current_version: str = "Frames"
    current_time_point: int = 0

    @classmethod
    def NewForSequence(
        cls,
        sequence: sequence_t,
        /,
        *,
        figure_name: str = "segmentation",
        archiver: archiver_t = None,
    ) -> tracking_2D_t:
        """
        Annotation-on-hover code adapted from:
        https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-in-matplotlib
        Answered by ImportanceOfBeingErnest on Nov 7 '17 at 20:23
        Edited by waterproof on Aug 12 '19 at 20:08
        """
        figure = pypl.figure()
        two_axes = figure.subplots(1, 2)

        axes_track = two_axes[0]
        axes_track.set_xlabel("time points")
        axes_track.set_ylabel("tracks")
        axes_track.yaxis.set_label_position("right")
        axes_track.yaxis.tick_right()
        axes_track.yaxis.set_ticks(
            range(1, sum(_tck.n_leaves for _tck in sequence.tracks) + 1)
        )

        axes_frame = two_axes[1]
        axes_frame.set_axis_off()

        colormap = colormap_t.get_cmap("plasma")
        mappable = colormap_t.ScalarMappable(cmap=colormap)
        figure.colorbar(mappable, ax=axes_track, location="left")

        all_versions = {"Frames": sequence.cell_frames}
        segmentations = sequence.segmentations
        for compartment, versions in segmentations.available_versions.items():
            for index, name, _ in versions:
                key = f"{compartment.name}:{index}:{name}"
                all_versions[key] = segmentations.CompartmentsWithVersion(
                    compartment, index=index
                )

        instance = cls(
            figure=figure,
            axes_track=axes_track,
            axes_frame=axes_frame,
            colormap=colormap,
            all_versions=all_versions,
        )

        all_cell_heights = []
        for t_idx, track in enumerate(sequence.tracks):
            if isinstance(track, single_track_t):
                PlotTrackEdges = instance._PlotSingleTrackEdges
            else:
                PlotTrackEdges = instance._PlotForkingTrackEdges
            PlotTrackEdges(track, all_cell_heights)

        scatter = axes_track.scatter(
            instance.time_points,
            all_cell_heights,
            marker="o",
            c=instance.colors,
            zorder=2,
        )
        annotation = axes_track.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox={"boxstyle": "round", "fc": "c"},
            arrowprops={"arrowstyle": "-"},
        )
        annotation.set_visible(False)
        frame = axes_frame.imshow(
            nmpy.zeros_like(sequence.cell_frames[0]),
            interpolation="nearest",
            cmap="gray",
        )

        instance.scatter = scatter
        instance.annotation = annotation
        instance.frame = frame

        figure.canvas.mpl_connect("motion_notify_event", instance._ShowAnnotation)
        figure.canvas.mpl_connect("button_press_event", instance._ShowNextFrame)

        axes_frame.set_title(instance.current_version)
        figure.tight_layout(h_pad=0.05)
        FinalizeDisplay(figure, figure_name, False, archiver)

        return instance

    def _PlotSingleTrackEdges(
        self,
        track: single_track_t,
        all_cell_heights: List[int],
        /,
    ) -> None:
        """"""
        length, time_points, label, where = self._ElementsForTrackPieces(track)

        self.labels.insert(where, track.root.label)
        self.time_points.insert(where, track.root_time_point)
        self.affinities.insert(where, 0.0)
        self.colors.insert(where, self.colormap(0.0))

        heights = (length + 1) * (label,)
        all_cell_heights.extend(heights)

        self.axes_track.plot(time_points, heights, color="gray", zorder=1)

    def _PlotForkingTrackEdges(
        self,
        track: forking_track_t,
        all_cell_heights: List[int],
        /,
    ) -> None:
        """"""
        with_int_labels = grph.convert_node_labels_to_integers(
            track, label_attribute="node_label"
        )
        int_layout = grph.nx_agraph.pygraphviz_layout(with_int_labels, prog="dot")
        positions = {
            with_int_labels.nodes[_idx]["node_label"]: _pst
            for _idx, _pst in int_layout.items()
        }

        all_time_points, all_heights = [], []
        min_height = max_height = positions[track.root][0]
        min_label = MAX_INTEGER
        root_height = None
        where = None
        for piece in track.Pieces():
            _, time_points, label, new_where = self._ElementsForTrackPieces(piece)
            heights = nmpy.fromiter(
                (positions[_cll][0] for _cll in piece), dtype=nmpy.float64
            )
            if piece[0] is track.root:
                root_height = heights[0]
            if where is None:
                where = new_where

            all_time_points.append(time_points)
            all_heights.append(heights)
            min_height = min(min_height, min(heights))
            max_height = max(max_height, max(heights))
            if (label is not None) and (label < min_label):
                min_label = label

        height_scaling = (track.n_leaves - 1) / (max_height - min_height)
        for time_points, heights in zip(all_time_points, all_heights):
            heights = height_scaling * (heights - min_height)
            heights = nmpy.around(heights) + min_label
            self.axes_track.plot(time_points, heights, color="gray", zorder=1)
            all_cell_heights.extend(heights[1:])
        root_height = (
            nmpy.around(height_scaling * (root_height - min_height)) + min_label
        )

        self.labels.insert(where, track.root.label)
        self.time_points.insert(where, track.root_time_point)
        self.affinities.insert(where, 0.0)
        self.colors.insert(where, self.colormap(0.0))

        all_cell_heights.insert(where, root_height)

    def _ElementsForTrackPieces(
        self,
        track: single_track_t,
        /,
    ) -> Tuple[int, Sequence[int], Optional[int], int]:
        """"""
        where = self.labels.__len__()

        root_time_point = track.root_time_point
        length = track.length
        label = track.label
        affinities = track.affinities

        time_points = tuple(range(root_time_point, root_time_point + length + 1))
        colors = tuple(self.colormap(_ffy) for _ffy in affinities)

        self.labels.extend(_cll.label for _cll in track[1:])
        self.time_points.extend(time_points[1:])
        self.affinities.extend(affinities)
        self.colors.extend(colors)

        return length, time_points, label, where

    def _ShowAnnotation(
        self,
        event: mouse_event_t,
        /,
    ) -> None:
        """"""
        inside = False

        if event.inaxes is self.axes_track:
            inside, details = self.scatter.contains(event)
            if inside:
                idx = details["ind"][0]
                time_point = self.time_points[idx]
                label = self.labels[idx]

                self.current_time_point = time_point

                position = self.scatter.get_offsets()[idx]
                text = (
                    f"Time {time_point}\nCell {label}\nPJcd {self.affinities[idx]:.2f}"
                )
                self.annotation.xy = position
                self.annotation.set_text(text)
                self.annotation.set_visible(True)

                display_frame = self.all_versions[self.current_version][time_point]
                self.frame.set_array(display_frame)
                self.frame.set_clim(nmpy.amin(display_frame), nmpy.amax(display_frame))

                for artist in self.axes_frame.get_children():
                    if isinstance(artist, annotation_t):
                        artist.remove()

                cell_frame = self.all_versions["Frames"][time_point]
                for cell in cell_frame.cells:
                    current_label = cell.label
                    if current_label == label:
                        color = "xkcd:electric blue"
                        font_weight = "bold"
                    else:
                        color = "red"
                        font_weight = "normal"
                    self.axes_frame.annotate(
                        str(current_label),
                        nmpy.flipud(cell.centroid),
                        ha="center",
                        fontsize="x-small",
                        fontweight=font_weight,
                        color=color,
                    )

                self.figure.canvas.draw_idle()

        if (not inside) and self.annotation.get_visible():
            self.annotation.set_visible(False)
            self.figure.canvas.draw_idle()

    def _ShowNextFrame(
        self,
        event: mouse_event_t,
        /,
    ) -> None:
        """"""
        if event.inaxes is self.axes_frame:
            all_names = tuple(self.all_versions.keys())
            where = all_names.index(self.current_version)
            where = (where + 1) % all_names.__len__()
            self.current_version = all_names[where]

            display_frame = self.all_versions[self.current_version][
                self.current_time_point
            ]
            self.frame.set_array(display_frame)
            self.frame.set_clim(nmpy.amin(display_frame), nmpy.amax(display_frame))

            self.axes_frame.set_title(self.current_version)

            self.figure.canvas.draw_idle()

    def ShowAndWait(self) -> None:
        """"""
        pypl.show()


def ShowTracking3D(
    sequence: sequence_t,
    /,
    *,
    with_track_labels: bool = True,
    with_cell_labels: bool = True,
    show_and_wait: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> None:
    """"""
    figure = pypl.figure()
    axes = figure.add_subplot(projection=axes_3d_t.name)
    axes.set_xlabel("row positions")
    axes.set_ylabel("column positions")
    axes.set_zlabel("time points")

    colors = tuple(CSS4COLORS.__members__.keys())
    max_time_point = 0
    for t_idx, track in enumerate(sequence.tracks):
        color_idx = t_idx % colors.__len__()

        for piece in track.Pieces():
            rows, cols, times, *labels = piece.AsRowsColsTimes(
                with_labels=with_cell_labels
            )
            if times[-1] > max_time_point:
                max_time_point = times[-1]

            axes.plot3D(rows, cols, times, colors[color_idx])

            if with_cell_labels:
                for row, col, time, label in zip(rows, cols, times, labels[0]):
                    axes.text(
                        row,
                        col,
                        time,
                        str(label),
                        fontsize="x-small",
                        color=colors[color_idx],
                    )
            if with_track_labels and (piece.label is not None):
                axes.text(
                    rows[-1],
                    cols[-1],
                    times[-1] + 0.25,
                    str(piece.label),
                    fontsize="x-small",
                    color=colors[color_idx],
                    bbox={
                        "facecolor": "none",
                        "edgecolor": colors[color_idx],
                        "boxstyle": "round",
                    },
                )

    FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


# Annotations of line plots
# import matplotlib.pyplot as plt
# import numpy as np; np.random.seed(1)
#
# x = np.sort(np.random.rand(15))
# y = np.sort(np.random.rand(15))
# names = np.array(list("ABCDEFGHIJKLMNO"))
#
# norm = plt.Normalize(1,4)
# cmap = plt.cm.RdYlGn
#
# fig,ax = plt.subplots()
# line, = plt.plot(x,y, marker="o")
#
# annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot.set_visible(False)
#
# def update_annot(ind):
#     x,y = line.get_data()
#     annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
#     text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
#                            " ".join([names[n] for n in ind["ind"]]))
#     annot.set_text(text)
#     annot.get_bbox_patch().set_alpha(0.4)
#
#
# def hover(event):
#     vis = annot.get_visible()
#     if event.inaxes == ax:
#         cont, ind = line.contains(event)
#         if cont:
#             update_annot(ind)
#             annot.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot.set_visible(False)
#                 fig.canvas.draw_idle()
#
# fig.canvas.mpl_connect("motion_notify_event", hover)
#
# plt.show()
