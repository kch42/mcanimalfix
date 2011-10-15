from distutils.core import setup
import py2exe

setup(
	name="mcanimalfix",
	version="1",
	description="Place animals on your Minecraft map after they got lost during the 1.8 update.",
	windows=[
		{
			"script": "animalfix.py"
		}
	],
	data_files=[("", ["README.markdown"])],
	options={
		"py2exe": {
			"optimize": 2,
			"excludes": ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
				"pywin.dialogs", "pywin.dialogs.list",
				"Tkconstants","Tkinter","tcl", "_ssl", "doctest", "pdb", "inspect", "wave", "email"
			  ],
			"includes": ["zlib"], # So the resulting program is able tu unpack the library, even after recompressing.
			"dll_excludes": ["MSVCP90.dll"],
			"bundle_files": 2
		}
	}
)
