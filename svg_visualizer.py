import matplotlib.pyplot as plt
from svgpathtools import svg2paths


def visualize_svg(uploaded_file):

    uploaded_file.seek(0)

    paths, attributes = svg2paths(uploaded_file)

    fig, ax = plt.subplots(figsize=(8, 8))

    for path in paths:

        points = []

        for seg in path:

            points.append((seg.start.real, seg.start.imag))
            points.append((seg.end.real, seg.end.imag))

        if points:

            x = [p[0] for p in points]
            y = [p[1] for p in points]

            ax.plot(x, y, linewidth=2)

    ax.set_title("SVG Shape Preview")

    ax.set_aspect('equal')

    ax.invert_yaxis()

    return fig
