#%%
from typing import Iterable
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
import numpy


def _orderByWeight(data_matrix: numpy.ndarray) -> numpy.ndarray:
    toret = numpy.zeros_like(data_matrix, dtype=int)
    for i in range(toret.shape[0]):
        toret[i] = numpy.argsort(data_matrix[i])

    return toret[:, ::-1]


def _orderByWeightReverse(data_matrix: numpy.ndarray) -> numpy.ndarray:
    toret = numpy.zeros_like(data_matrix, dtype=int)
    for i in range(toret.shape[0]):
        toret[i] = numpy.argsort(data_matrix[i])

    return toret


def _orderByNone(data_matrix: numpy.ndarray) -> numpy.ndarray:
    toret = numpy.zeros_like(data_matrix, dtype=int)
    for i in range(toret.shape[0]):
        toret[:, i] = i

    return toret


def _orderByPosition(data_matrix: numpy.ndarray) -> numpy.ndarray:
    n = data_matrix.shape[0]
    t = list(range(n))
    half = n // 2
    toret = numpy.zeros_like(data_matrix, dtype=int)
    for i in range(toret.shape[0]):
        f = -(half - i)
        toret[:, i] = numpy.array(t[f:] + t[:f])
    return toret  # [:, ::-1]


def _prepareBases(
    data_matrix: numpy.ndarray, gap: float
) -> "tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]":
    """get the ideogram ends in degrees

    Args:
        data_matrix (numpy.ndarray): the working matrix
        gap (float): the gap between the id, in degrees

    Returns:
        tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]: returns the sum of the row, the length of the bases in degrees and the angular limits of the bases
    """
    L = data_matrix.shape[1]
    row_sum = numpy.sum(data_matrix, axis=1)
    ideogram_length = (360.0 - gap * L) * row_sum / numpy.sum(row_sum)
    ideo_ends = numpy.zeros((len(ideogram_length), 2))
    left = 0
    for k in range(len(ideogram_length)):
        right = left + ideogram_length[k]
        ideo_ends[k, :] = [left, right]
        left = right + gap
    return row_sum, ideogram_length, ideo_ends


def _bezierArcMaker(
    start: "numpy.array", end: "numpy.array", center: "numpy.array"
) -> "list[numpy.array]":
    """gets the two mid control points for generating an approximation of an arc with a cubic bezier

    Args:
        start (numpy.array): the start point
        end (numpy.array): the end point
        center (numpy.array): the center of the circumference

    Returns:
        list[numpy.array]: _description_
    """
    # source https://stackoverflow.com/a/44829356

    # TODO: se up a maximum 45 or 90 degree for the aproximation
    c = numpy.array([center[0], center[1]], dtype=float)
    p1 = numpy.array([start[0], start[1]], dtype=float)
    p4 = numpy.array([end[0], end[1]], dtype=float)
    a = p1 - c
    b = p4 - c
    q1 = a.dot(a)
    q2 = q1 + a.dot(b)
    k2 = (4.0 / 3.0) * (numpy.sqrt(2 * q1 * q2) - q2) / (a[0] * b[1] - a[1] * b[0])
    p2 = c + a + k2 * numpy.array([-a[1], a[0]])
    p3 = c + b + k2 * numpy.array([b[1], -b[0]])
    return [p2, p3]


def _ribbonCoordMaker(
    data_matrix: numpy.ndarray,
    row_value: numpy.ndarray,
    ideogram_length: numpy.ndarray,
    ideo_ends: numpy.ndarray,
    ignoreLessThan: int = 1,
    onlyFlux: bool = False,
    ordering: str = "matrix",
) -> "list[dict]":
    # TODO:add ordering:
    # - matrix do not does nothing
    # - leftright put the self in the center
    # - weight reorders the entries for each from the bigger
    # - weightr reorders the entries for each from the smaller
    orders = _orderByNone(data_matrix)
    if ordering == "leftright" or ordering == "position":
        orders = _orderByPosition(data_matrix)
    elif ordering == "weight":
        orders = _orderByWeight(data_matrix)
    elif ordering == "weightr":
        orders = _orderByWeightReverse(data_matrix)
    # mapped is a conversion of the values of the matrix in fracrion of the circumerence
    mapped = numpy.zeros(data_matrix.shape, dtype=float)
    dataLenght = data_matrix.shape[0]
    for j in range(dataLenght):
        mapped[:, j] = ideogram_length * data_matrix[:, j] / row_value
    ribbon_boundary = numpy.zeros((dataLenght, dataLenght, 2), dtype=float)
    for i in range(dataLenght):
        start = ideo_ends[i][0]
        # ribbon_boundary[i, orders[0]] = start
        for j in range(dataLenght):

            ribbon_boundary[i, orders[i, j], 0] = start
            ribbon_boundary[i, orders[i, j], 1] = start + mapped[i, orders[i, j]]

            start = ribbon_boundary[i, orders[i, j], 1]

    ribbons = []
    for i in range(dataLenght):
        for j in range(i + 1, dataLenght):
            if (
                data_matrix[i, j] < ignoreLessThan
                and data_matrix[j, i] < ignoreLessThan
            ):
                continue
            high, low = (i, j) if data_matrix[i, j] > data_matrix[j, i] else (j, i)

            ribbons.append(
                dict(
                    kind="flux" + ("ToZero" if data_matrix[low, high] == 0 else ""),
                    high=high,
                    low=low,
                    anglesHigh=(
                        ribbon_boundary[high, low, 0],
                        ribbon_boundary[high, low, 1],
                    ),
                    anglesLow=(
                        ribbon_boundary[low, high, 1],
                        ribbon_boundary[low, high, 0],
                    ),
                )
            )
    if not onlyFlux:
        for i in range(dataLenght):
            ribbons.append(
                dict(
                    kind="self",
                    id=i,
                    angles=(
                        ribbon_boundary[i, i, 0],
                        ribbon_boundary[i, i, 1],
                    ),
                )
            )

    return ribbons


def ChordDiagram(
    matrix: "list[list]",
    colors: Iterable = None,
    labels: list = None,
    ax: "plt.Axes|None" = None,
    GAP: float = numpy.rad2deg(2 * numpy.pi * 0.005),
    radius: float = 0.5,
    width: float = 0.05,
    ribbonposShift: float = 0.7,
    labelpos: float = 1.0,
    labelskwargs: dict = dict(),
    visualizationScale: float = 1.0,
    ignoreLessThan: int = 1,
    onlyFlux: bool = False,
    ordering: str = "matrix",
):
    if not ax:
        fig, ax = plt.subplots(1, figsize=(10, 10))
    ax.axis("off")
    ax.set_xlim(numpy.array([-1.0, 1.0]) * radius / visualizationScale)
    ax.set_ylim(numpy.array([-1.0, 1.0]) * radius / visualizationScale)
    ax.set_box_aspect(1)

    center = numpy.array([0.0, 0.0])
    wmatrix = numpy.array(matrix, dtype=int)
    row_sum, ideogram_length, ideo_ends = _prepareBases(wmatrix, GAP)
    myribbons = _ribbonCoordMaker(
        wmatrix,
        row_sum,
        ideogram_length,
        ideo_ends,
        ignoreLessThan=ignoreLessThan,
        onlyFlux=onlyFlux,
        ordering=ordering,
    )

    def getPos(x):
        return numpy.array([numpy.cos(numpy.deg2rad(x)), numpy.sin(numpy.deg2rad(x))])

    ribbonPos = radius - width * ribbonposShift
    FLUXPATH = [
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    FLUXTOZEROPATH = [
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    SELFPATH = [
        Path.MOVETO,
        Path.CURVE3,
        Path.CURVE3,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    for ribbon in myribbons:
        if ribbon["kind"] == "flux" or ribbon["kind"] == "fluxToZero":
            as1, as2 = ribbon["anglesHigh"]
            ae1, ae2 = ribbon["anglesLow"]
            s1 = center + ribbonPos * getPos(as1)
            s2 = center + ribbonPos * getPos(as2)
            s4, s3 = _bezierArcMaker(s2, s1, center)
            e1 = center + ribbonPos * getPos(ae1)
            e2 = center + ribbonPos * getPos(ae2)
            e3, e4 = _bezierArcMaker(e1, e2, center)
            ribbonPath = PathPatch(
                Path(
                    [s1, center, e1, e3, e4, e2, center, s2, s4, s3, s1, s1]
                    if ribbon["kind"] == "flux"
                    else [s1, center, e1, center, s2, s4, s3, s1, s1],
                    FLUXPATH if ribbon["kind"] == "flux" else FLUXTOZEROPATH,
                ),
                transform=ax.transData,
                alpha=0.4,
                zorder=1,
            )
            if colors is not None:
                ribbonPath.set(color=colors[ribbon["high"]])
            ax.add_patch(ribbonPath)
        elif ribbon["kind"] == "self":
            as1, as2 = ribbon["angles"]
            s1 = center + ribbonPos * getPos(as1)
            s2 = center + ribbonPos * getPos(as2)
            s4, s3 = _bezierArcMaker(s2, s1, center)

            ribbonPath = PathPatch(
                Path(
                    [s1, center, s2, s4, s3, s1, s1],
                    SELFPATH,
                ),
                # fc="none",
                transform=ax.transData,
                alpha=0.4,
                zorder=1,
            )
            if colors is not None:
                ribbonPath.set(color=colors[ribbon["id"]])
            ax.add_patch(ribbonPath)

    if width > 0:
        arcs = [Wedge(center, radius, a[0], a[1], width=width) for a in ideo_ends]

        p = PatchCollection(arcs, zorder=2)
        if colors is not None:
            p.set(color=colors)
        ax.add_collection(p)

    if labels:
        for i, a in enumerate(ideo_ends):
            pos = center + labelpos * radius * getPos(0.5 * (a[0] + a[1]))
            ax.text(pos[0], pos[1], labels[i], ha="center", va="center", **labelskwargs)


if __name__ == "__main__":
    for t in [
        [[10, 2, 1, 5], [10, 2, 1, 4], [2, 10, 2, 3], [2, 2, 2, 2]],
        [[10, 2, 1], [10, 2, 1], [2, 10, 2]],
    ]:
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        ChordDiagram(
            t,
            ax=ax[0],
            colors=["#00F", "#F00", "#0F0", "#0FF"],
            labels=["0", "1", "2", "3"],
            labelpos=1.5,
            # width=0,
            # onlyFlux=True,
            # GAP=10,
            # ignoreLessThan=10,
            labelskwargs=dict(),
        )
        ChordDiagram(
            t,
            ax=ax[1],
            colors=["#00F", "#F00", "#0F0", "#0FF"],
            labels=["0", "1", "2", "3"],
            # width=0,
            # onlyFlux=True,
            # GAP=10,
            # ignoreLessThan=10,
            ordering="position",
            labelskwargs=dict(),
        )
        ChordDiagram(
            t,
            ax=ax[2],
            colors=["#00F", "#F00", "#0F0", "#0FF"],
            labels=["0", "1", "2", "3"],
            # width=0,
            # onlyFlux=True,
            # GAP=10,
            # ignoreLessThan=10,
            ordering="weight",
            labelskwargs=dict(),
            visualizationScale=0.5,
        )
