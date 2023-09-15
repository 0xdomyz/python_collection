# python example that makes 2 png time series plot
######################################################
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

here = "office/ppt"

# seed
np.random.seed(123)

# ts example
data = pd.DataFrame(
    np.random.randn(10, 4),
    index=pd.date_range("1/1/2000", periods=10),
    columns=list("ABCD"),
)

# plot and save as png
data.plot()
plt.savefig(f"{here}/ts.png")

# another ts example
data = data * 20
data.plot()
plt.savefig(f"{here}/ts2.png")


# python example that puts 2 png on dir to a ppt
######################################################
from pathlib import Path

import pptx.util
from pptx import Presentation

# get pngs
pngs = [i.as_posix() for i in Path(here).glob("*.png")]

# delete ppt if exists
ppt = Path(f"{here}/ts.pptx")
if ppt.exists():
    ppt.unlink()

# make ppt
prs = Presentation()

for png in pngs:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # add pic in the middle of the slide
    left = top = pptx.util.Inches(1)
    pic = slide.shapes.add_picture(png, left, top)

prs.save(f"{here}/ts.pptx")


# functionalise
def add_pngs(prs, pngs):
    for png in pngs:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        # add pic in the middle of the slide
        left = top = pptx.util.Inches(1)
        pic = slide.shapes.add_picture(png, left, top)


def add_2pngs(prs, png1, png2):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # add pic left and right
    left = pptx.util.Inches(1)
    top = pptx.util.Inches(1)
    pic = slide.shapes.add_picture(png1, left, top)
    left = pptx.util.Inches(4)
    top = pptx.util.Inches(1)
    pic = slide.shapes.add_picture(png2, left, top)


# a title page
######################################################
# make ppt
prs = Presentation()

# title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Office"
subtitle.text = "subtitle"

prs.save(f"{here}/title.pptx")


# functionalise
def add_title(prs, title_text, subtitle_text):
    # title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = title_text
    subtitle.text = subtitle_text


# orchestrate
###########################

# delete ppt if exists
ppt = Path(f"{here}/orchestrate.pptx")
if ppt.exists():
    ppt.unlink()

# make ppt
prs = Presentation()

# a title slide and 2 pngs
add_title(prs, "Office", "subtitle")
add_pngs(prs, pngs)

# another title slide and 2 pngs
add_title(prs, "Office2", "subtitle2")
add_pngs(prs, pngs)

prs.save(f"{here}/orchestrate.pptx")
