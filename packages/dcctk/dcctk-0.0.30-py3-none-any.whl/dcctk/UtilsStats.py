from scipy import spatial

def cossim(x, y) -> float:
    """[summary]

    Parameters
    ----------
    x : [type]
        [description]
    y : [type]
        [description]

    Returns
    -------
    float
        [description]
    """
    return 1 - spatial.distance.cosine(x, y)
