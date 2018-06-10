from distutils.core import setup

setup(
	name="project1",
	version="1.0",
	packages=["ih"],
	license="GPL",
	scripts=[
		"scripts/bitwise-and",
		"scripts/bitwise-not",
		"scripts/bitwise-or",
		"scripts/bitwise-xor",
		"scripts/convert-color",
		"scripts/meanshift",
		"scripts/threshold",
		"scripts/extract",
		"scripts/adaptive-threshold",
		"scripts/blur",
		"scripts/gaussian-blur",
		"scripts/median-blur",
		"scripts/normalize-intensity",
		"scripts/morphology",
		"scripts/crop",
		"scripts/fill",
		"scripts/contour-cut",
		"scripts/contour-chop",
		"scripts/edges",
		"scripts/color-filter",
		"scripts/resize",
        "scripts/mask",
		"scripts/add-weighted",
		"scripts/split",
		"scripts/equalize-hist",
		"scripts/flood-fill",

		"scripts/seed",

		"scripts/extract-multi",
		"scripts/osg-wrapper.sh",

		"scripts/ih-data",

	]
)
