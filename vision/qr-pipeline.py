"""
Pipeline from image of qr code to sending its value.
"""
import cv2
import numpy as np
from scipy.signal import argrelextrema

from generator.QrCode import QrCode
from normalize.edges import get_edges
from normalize.ts_converter import get_ts_verticies, binarize_mat
from accumulator.py_to_cpp import TS


if __name__ == '__main__':
    value = '1234'

    generator = QrCode(value)

    # switch to each corners
    image = generator.img

    # cv2.imshow("qr", image)
    # cv2.waitKey(0)

    edges = binarize_mat(get_edges(image), threshold=.5)

    # cv2.imshow("edges", edges)
    # cv2.waitKey(0)

    verticies = get_ts_verticies(edges, u=10, z=0.)

    vertex_count = len(verticies) // 3 
 
    space = TS(1024, 768, vertex_count, verticies.ctypes.data)
    accumulated = space.accumulate()

    # out = np.where(accumulated > 0, .2, 0.)
    # cv2.imshow("img", out)
    # cv2.waitKey(0)

    maxima = argrelextrema(accumulated, np.greater)
    X, Y = maxima

    # (optional) Find N highest maxima
    print(maxima)

    # hypothesis testing w/ 3 points
    """
    Testing hypotheses about the vanishing points.
    Each of the two parts of the T S space is searched for the
    vanishing point and the corresponding group of projected
    parallel lines. First, N highest local maxima are found in
    the accumulator space (see Figure 3a). These maxima are
    used for generating hypotheses about the vanishing points
    and the corresponding groups of concurrent lines. One hypothesis is defined by 3 local maxima (i.e. triplets are drawn
    out of the N points) and it uniquely defines a spatial distribution of local maxima corresponding to the group of perspectively projected parallel lines. The confidence score for
    each hypothesis calculates the similarity of real and estimated maxima and minima.
    """
    """
    Figure 3: a) Two accumulation areas with 16 best found
    maxima. These 16 maxima are used for generating the hypotheses. b) One generated hypothesis for each half of the
    T S space. A line is approximated by 3 random maxima.
    The T S space is searched along the line and a score of the
    hypothesis is computed.
    """


    # extract marker bitmap
    """
    For sampling the input image in the center of each module, the minima
    between two consecutive maxima are used (see Figure 3b).
    A Cartesian product of the two groups of minima in the
    Hough space determines individual modules of the marker.
    These modules are extracted and they form a low-resolution
    bitmap which is searched for the synchronization patterns
    and further processed (see Figure 4).
    """    

    # Rapid Detection of Regions with a Possible QR code
    # Extraction of the Histogram of Oriented Gradients
    """
    To get an indicator for QR code presence, the algorithm
    first extracts the Histogram of Oriented Gradients (HOG)
    for each tile. For each pixel, the algorithm computes the
    size of the gradient: both its magnitude and orientation.
    Only gradients whose magnitude exceeds a given conservative threshold are processed (just as in Section 3). The
    threshold is set fairly low so that a reasonable amount of
    blur does not spoil the detection. The stored edge pixels are
    used to create the HOG for the tile. We used a histogram
    with a low number of bins (e.g. 12 bins); higher histogram
    resolution is futile due to the limitations of gradient direction precision. The resulting histogram is a vector for each
    tile: h = Hn(T (u, v)), where n is the number of bins (see
    Figure 6 for HOG representation. The highlighted red and
    blue bins of the HOGs are the detected two dominant edge
    orientations.)
    To speed up the process, the histograms can be approximated by taking only pixels along scanlines vertically and
    horizontally separated by a given number of pixels. By processing only the scanlines, only a small percentage of input
    image pixels have to be processed for each tile, but still have
    a precise-enough approximation of the HOG.
    """

    # Feature Vector Extraction
    """
    . In addition to the gradient
    histogram, a feature vector is computed for each tile. It
    contains the normalized histogram and four additional values: corresponding angles of the two main gradient directions in the histogram, the number of edge pixels per unit
    area and an estimation of the probability score of a chessboard like structure in the tile based on the histogram. Let
    then v = (p, α1, α2, Ne
    A , hnorm) be the feature vector for a
    tile with normalized histogram hnorm, pixel area A, and the
    number of edge pixels over a threshold Ne. The probability 
    score is computed in the following way:
    p = (1 − (||α1 − α2| − π/2 |) / π/2) * (2 min(ha, hb)) / (ha + hb)
    where ha and hb are the values in the histogram corresponding to the 
    two dominant edge orientations. The first term
    ensures that the two dominant directions are approximately π/ 2 apart; 
    the second term prefers equally high peaks in the histogram.
    The two main gradient directions detected from the HOG α1
    and α2 meet an additional constraint that |α1−π/2 | << |α2−π/2 |
    or α1 < α2. The order of the angles is important for the
    segmentation.
    """

    # Segmentation of tiles
    """
    This vector of features can be
    used for segmentation of the tiles. For segmentation we currently use a simple 4-neighborhood blob coloring [Rosenfeld
    and Pfaltz 1966], which requires two passes for each level in
    the hierarchy of tiles. We used only the first angle α1, the
    probability score p and the edge density Ne
    A for segmentation for performance reasons. The segmentation is done on a
    relatively small number of elements, so it does not introduce
    any major computational overhead.
    The result of the segmentation (Figure 7) is a set of connected tiles {S1, S2,...,Sk}, k ∈ N. If A(Sk) is the area
    of the axis-aligned bounding box in pixel2 and then let the
    probability score that the segment is a possible position of
    a QR code be:
    P(Si) = 1/A(Si) * sum(p * Ne/A) for T in Si, i in {0, .. k}
    where p and Ne/A are values from the feature vector for tile T .
    """

    # Segment Classification
    """
    Based on the computed score
    P(Si) and the shape of a set of tiles Si we use a binary
    classifier to determine whether the area covered by a given
    segment should be further processed to find QR codes:

    C(Si) = {1 if P(Si) ≥ T (is a possible position)
            {0 otherwise (not a probable position) 

    where T is an experimentally acquired threshold. The regions classified as probable positions of a 2D barcode in our
    example in Figure 6 are represented by thick yellow rectangles.
    An example of the segmentation is shown in Figure 7. The
    edge length of the tiles in this case were w = 120 pixels.
    Two of four QR codes were precisely localized. The segment
    corresponding to the third, bigger one on the left side of the
    image contains also some parts of the text, since at this resolution it has properties similar to the QR code itself. The
    fact that the QR code candidate rectangle does not tightly
    fit the actual code edges does not prevent it from being detectable by the detection/recognition algorithm. The fourth
    blurred QR code in the background did not get localized
    due to the small number of edge pixels and the near uniform
    distribution of the gradient directions.
    """

    # Multiscale Processing
    """
    The size of the tiles can have a major effect on the success
    of finding correct candidate positions. Choosing too large region 
    size might cause overlooking small matrix codes. For
    example, when a small QR code surrounded by large noise
    covers only a small part of four neighboring tiles, the probability 
    score of a regular structure in the four tiles would be
    very small. On the other hand, choosing too small tile size
    w would cover only a small part of a large QR code and the
    segmentation would fail to group the tiles covered by the
    QR code.
    We propose using a quad-tree of tiles Tl(u, v), where l is the
    level. The HOG and edge extraction have to be computed
    only at the lowest level l = 1. The histogram of the tiles
    at a higher level in the hierarchy can be computed simply
    by accumulating the corresponding bins of the histograms of
    the child tiles:
    Hn(Tl(u, v)) = sum(sum(Hn(T[l-1](2u+i, 2v+j))) for j=0 to 1) for i=0 to 1
    The segmentation and classification of the segments can be
    done at each level (or alternatively, a hierarchical segmentation 
    can be used). Since the gradients and edge pixels
    are not recomputed for higher levels and the number of segments is 
    relatively low, so this does not mean a significant
    computational overhead.
    The whole algorithm for detection of QR codes in a highresolution 
    image is depicted in Algorithm 1.
    """