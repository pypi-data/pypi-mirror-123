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
from enum import Enum as enum_t
from typing import Callable, ClassVar, Dict, List, Sequence, Tuple

import numpy as nmpy
import scipy.ndimage.morphology as scph
import scipy.optimize as spop
import skimage.morphology as mrph
import skimage.segmentation as sgmt
from scipy import ndimage as image_t
from scipy.spatial import distance as dstc

from cell_tracking_BC.task.jaccard import PseudoJaccard


array_t = nmpy.ndarray


class compartment_t(enum_t):
    CELL = 0
    CYTOPLASM = 1
    NUCLEUS = 2


version_dict_h = Dict[compartment_t, Dict[str, array_t]]


def _VersionDict() -> version_dict_h:
    """"""
    return {_key: {} for _key in compartment_t}


@dtcl.dataclass(repr=False, eq=False)
class segmentation_t:

    IDX_NAME_SEP: ClassVar[str] = "-"

    cell: array_t = None
    cytoplasm: array_t = None
    nucleus: array_t = None
    version_idx: int = 0
    version_name: str = f"0{IDX_NAME_SEP}original"
    versions: version_dict_h = dtcl.field(init=False, default_factory=_VersionDict)

    @classmethod
    def NewFromCompartments(
        cls,
        /,
        *,
        cell: array_t = None,
        cytoplasm: array_t = None,
        nucleus: array_t = None,
    ) -> segmentation_t:
        """
        Valid options:
            - cell               => cytoplasm = None, nucleus = None
            - cell, cytoplasm    => nucleus = cell - cytoplasm
            - cell, nucleus      => cytoplasm = cell - nucleus
            - cytoplasm          => cell = filled cytoplasm, nucleus = cell - cytoplasm
            - cytoplasm, nucleus => cell = cytoplasm + nucleus
        """
        filled_cytoplasm = None
        if (cell is None) and (cytoplasm is None):
            raise ValueError("Cytoplasm and cell arrays both None")
        if not ((cell is None) or (cytoplasm is None) or (nucleus is None)):
            raise ValueError("Nucleus, cytoplasm and cell arrays all not None")
        if not ((cell is None) or (cytoplasm is None)):
            filled_cytoplasm = scph.binary_fill_holes(cytoplasm)
            if not nmpy.array_equal(filled_cytoplasm, cell):
                raise ValueError("Cytoplasm outer borders do not coincide with cells")
        if not ((cell is None) or (nucleus is None)):
            if nmpy.any(cell[nucleus.astype(nmpy.bool, copy=False)] == 0):
                raise ValueError("Nuclei outer borders not restricted to cells")
        if not ((cytoplasm is None) or (nucleus is None)):
            if nmpy.any(cytoplasm[nucleus.astype(nmpy.bool, copy=False)] == 1):
                raise ValueError("Cytoplasm and nucleus arrays intersect")
            # Necessarily not already computed above since all 3 segmentations cannot be passed
            filled_cytoplasm = scph.binary_fill_holes(cytoplasm)
            union = nmpy.logical_or(cytoplasm, nucleus)
            if not nmpy.array_equal(filled_cytoplasm, union):
                raise ValueError("Cytoplasm inner borders do not coincide with nuclei")

        if cell is None:  # Then cytoplasm is not None
            if filled_cytoplasm is None:
                if nucleus is None:
                    cell = scph.binary_fill_holes(cytoplasm)
                else:
                    cell = cytoplasm.copy()
                    cell[nucleus] = 1
            else:
                cell = filled_cytoplasm
        # From then on, cell is not None
        if (cytoplasm is None) and (nucleus is not None):
            cytoplasm = cell.copy()
            cytoplasm[nucleus] = 0
        elif (nucleus is None) and (cytoplasm is not None):
            nucleus = cell.copy()
            nucleus[cytoplasm] = 0

        return cls(cell=cell, cytoplasm=cytoplasm, nucleus=nucleus)

    def ClearBorderObjects(self) -> None:
        """"""
        if self.nucleus is None:
            if self.cytoplasm is None:
                segmentations = [self.cell]
                names = (compartment_t.CELL,)
            else:
                segmentations = [self.cytoplasm, self.cell]
                names = (compartment_t.CYTOPLASM, compartment_t.CELL)
        else:
            if self.cytoplasm is None:
                segmentations = [self.nucleus, self.cell]
                names = (compartment_t.NUCLEUS, compartment_t.CELL)
            else:
                segmentations = [self.nucleus, self.cytoplasm]
                names = (compartment_t.NUCLEUS, compartment_t.CYTOPLASM)

        # --- Clear outer segmentation border objects
        has_changed = self._ClearBorderObjects(segmentations, names, -1)

        if segmentations.__len__() > 1:
            # --- Clear inner segmentation border objects
            segmentation = segmentations[0]
            name = names[0]
            if segmentation is self.cytoplasm:
                has_changed |= self._ClearBorderObjects(segmentations, names, 0)
            else:
                dilated = mrph.dilation(segmentation)
                labeled, n_objects = mrph.label(
                    dilated, return_num=True, connectivity=1
                )
                for label in range(1, n_objects + 1):
                    where_label = labeled == label
                    if nmpy.any(segmentations[1][where_label] > 0):
                        pass
                    else:
                        dilated[where_label] = 0
                original = segmentation.copy()
                segmentation[dilated == 0] = 0
                if not nmpy.array_equal(segmentation, original):
                    self.versions[name][self.version_name] = original
                    has_changed = True

        if has_changed:
            self.version_idx += 1
            self.version_name = (
                f"{self.version_idx}{self.__class__.IDX_NAME_SEP}cleared borders"
            )

    def _ClearBorderObjects(
        self, segmentations: List[array_t], names: Sequence[compartment_t], idx: int, /
    ) -> bool:
        """"""
        segmentation = segmentations[idx]
        original = segmentation.copy()

        sgmt.clear_border(segmentation, in_place=True)

        if nmpy.array_equal(segmentation, original):
            return False

        self.versions[names[idx]][self.version_name] = original

        return True

    def FilterCellsOut(
        self,
        CellIsInvalid: Callable[[int, array_t, dict], bool],
        /,
        **kwargs,
    ) -> None:
        """
        Currently, only applicable to the cell segmentation when no other compartments are present

        Parameters
        ----------
        CellIsInvalid: Arguments are: cell label (from 1), labeled segmentation, and (optional) keyword arguments
        kwargs: Passed to CellIsInvalid as keyword arguments

        Returns
        -------
        """
        assert (self.cytoplasm is None) and (self.nucleus is None)

        segmentation = self.cell

        labeled, n_cells = mrph.label(segmentation, return_num=True, connectivity=1)
        invalids = []
        for label in range(1, n_cells + 1):
            if CellIsInvalid(label, labeled, **kwargs):
                invalids.append(label)

        if invalids.__len__() > 0:
            original = segmentation.copy()
            for label in invalids:
                segmentation[labeled == label] = 0
            self.versions[compartment_t.CELL][self.version_name] = original

            self.version_idx += 1
            self.version_name = (
                f"{self.version_idx}{self.__class__.IDX_NAME_SEP}filtered cells"
            )

    def CorrectBasedOnTemporalCoherence(
        self,
        previous: segmentation_t,
        /,
        *,
        min_jaccard: float = 0.75,
        max_area_discrepancy: float = 0.25,
    ) -> None:
        """
        min_jaccard: Actually, Pseudo-Jaccard

        Currently, only applicable to the cell segmentation when no other compartments are present
        """
        assert (self.cytoplasm is None) and (self.nucleus is None)

        segmentation = self.cell
        previous = previous.cell

        labeled, n_cells = mrph.label(segmentation, return_num=True, connectivity=1)
        labeled_previous, n_cells_previous = mrph.label(
            previous, return_num=True, connectivity=1
        )

        cells_idc = nmpy.fromiter(range(1, n_cells + 1), dtype=nmpy.uint64)
        cells_idc_previous = nmpy.fromiter(
            range(1, n_cells_previous + 1), dtype=nmpy.uint64
        )
        # Note the reversed parameter order in PseudoJaccard since a fusion is a division in reversed time
        _PseudoJaccard = lambda idx_1, idx_2: PseudoJaccard(
            labeled, labeled_previous, idx_2, idx_1
        )
        pairwise_jaccards = dstc.cdist(
            cells_idc_previous[:, None], cells_idc[:, None], metric=_PseudoJaccard
        )

        tp1_to_t_associations = {}
        while True:
            row_ind, col_ind = spop.linear_sum_assignment(1.0 - pairwise_jaccards)
            valid_idc = pairwise_jaccards[row_ind, col_ind] > min_jaccard
            if not nmpy.any(valid_idc):
                break
            for key, value in zip(col_ind[valid_idc], row_ind[valid_idc]):
                if key in tp1_to_t_associations:
                    tp1_to_t_associations[key].append(value)
                else:
                    tp1_to_t_associations[key] = [value]
            pairwise_jaccards[row_ind, :] = 0.0

        has_changed = False
        for label in range(1, n_cells + 1):
            previous_labels = tp1_to_t_associations.get(label - 1)
            if (previous_labels is not None) and (previous_labels.__len__() > 1):
                previous_labels = nmpy.array(previous_labels)
                previous_labels += 1

                where_fused = labeled == label
                fused_area = nmpy.count_nonzero(where_fused)

                seeds = nmpy.zeros_like(labeled_previous)
                for l_idx, previous_label in enumerate(previous_labels, start=1):
                    seeds[labeled_previous == previous_label] = l_idx
                seeds_area = nmpy.count_nonzero(seeds)
                if (
                    discrepancy := abs(seeds_area - fused_area) / fused_area
                ) > max_area_discrepancy:
                    print(
                        f"/!\\ Segmentation correction discarded due to high t-total-area/(t+1)-fused-area discrepancy "
                        f"({discrepancy}) between cells {previous_labels} and fused cell {label}"
                    )
                    continue

                seeds[nmpy.logical_not(where_fused)] = 0
                # Just in case zeroing the non-fused region deleted some labels. If this can happen, it must be in very
                # pathological cases.
                seeds, *_ = sgmt.relabel_sequential(seeds)
                if (n_seeds := nmpy.amax(seeds)) != previous_labels.size:
                    # Should never happen (see comment above)
                    print(
                        f"/!\\ Segmentation correction discarded due to invalid watershed seeds: "
                        f"Actual={n_seeds}; Expected={previous_labels.size}"
                    )
                    continue

                distance_map = image_t.distance_transform_edt(where_fused)
                separated = sgmt.watershed(
                    -distance_map, seeds, mask=where_fused, watershed_line=True
                )

                original = segmentation.copy()
                segmentation[where_fused] = 0
                segmentation[separated > 0] = 1
                if not nmpy.array_equal(segmentation, original):
                    self.versions[compartment_t.CELL][self.version_name] = original
                    has_changed = True

        if has_changed:
            self.version_idx += 1
            self.version_name = (
                f"{self.version_idx}{self.__class__.IDX_NAME_SEP}corrected w/ temp-corr"
            )

    def NonNoneAsList(self) -> Tuple[List[array_t], Sequence[str]]:
        """
        For preparing calls to cell_tracking_BC.type.cell_t.NewFromMaps
        """
        if self.nucleus is None:
            if self.cytoplasm is None:
                segmentations = [self.cell]
                parameters = ("cell_map",)
            else:
                segmentations = [self.cytoplasm, self.cell]
                parameters = ("cytoplasm_map", "cell_map")
        else:
            if self.cytoplasm is None:
                segmentations = [self.nucleus, self.cell]
                parameters = ("nucleus_map", "cell_map")
            else:
                segmentations = [self.nucleus, self.cytoplasm]
                parameters = ("nucleus_map", "cytoplasm_map")

        return segmentations, parameters

    @property
    def available_versions(self) -> Dict[compartment_t, Sequence[Tuple[int, str, str]]]:
        """
        The per-compartment sequences contain tuples (version index, version basename, version name), where version name
        is a combination of version index and basename.
        """
        output = {_key: [] for _key in compartment_t}

        for compartment in compartment_t:
            versions = output[compartment]

            if compartment is compartment_t.CELL:
                segmentation = self.cell
            elif compartment is compartment_t.CYTOPLASM:
                segmentation = self.cytoplasm
            else:
                segmentation = self.nucleus
            if segmentation is not None:
                _, name = self.version_name.split(
                    sep=self.__class__.IDX_NAME_SEP, maxsplit=1
                )
                versions.append((self.version_idx, name, self.version_name))

            for key in self.versions[compartment].keys():
                index, name = key.split(sep=self.__class__.IDX_NAME_SEP, maxsplit=1)
                versions.append((int(index), name, key))

        emptys = []
        for key, value in output.items():
            if value.__len__() == 0:
                emptys.append(key)
        for empty in emptys:
            del output[empty]

        return output

    def CompartmentWithVersion(
        self, compartment: compartment_t, /, *, index: int = None, name: str = None
    ) -> array_t:
        """
        index: if None and name is None also, then returns latest version
        If both index and name are passed, name is ignored.
        """
        if (
            ((index is None) and (name is None))
            or (index == self.version_idx)
            or (self.version_name.endswith(f"{self.__class__.IDX_NAME_SEP}{name}"))
        ):
            if compartment is compartment_t.CELL:
                return self.cell
            if compartment is compartment_t.CYTOPLASM:
                if self.cytoplasm is not None:
                    return self.cytoplasm
            elif compartment is compartment_t.NUCLEUS:
                if self.nucleus is not None:
                    return self.nucleus
        else:
            if index is not None:
                VersionIsAMatch = lambda _ver: _ver.startswith(
                    f"{index}{self.__class__.IDX_NAME_SEP}"
                )
            else:
                VersionIsAMatch = lambda _ver: _ver.endswith(
                    f"{self.__class__.IDX_NAME_SEP}{name}"
                )
            for key, value in self.versions[compartment].items():
                if VersionIsAMatch(key):
                    return value

        known_versions = tuple(
            _key.name + ": " + ", ".join(_ver[2] for _ver in _val)
            for _key, _val in self.available_versions.items()
        )
        known_versions = "\n    ".join(known_versions)
        raise ValueError(
            f"{compartment}/{index}/{name}: Invalid compartment, version index, "
            f"and/or version name specification; Expected among\n    {known_versions}"
        )
