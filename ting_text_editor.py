#!/usr/bin/env python3

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

#global variables
filename = "Untitled";

def button_save_clicked(self):
	buff = textview.get_buffer() #get the textview buffer
	text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True) # get all the text from buffer
	global filename # use the global filename variable
	if filename == "Untitled": # if new file use save as instead
		button_save_as_clicked(self)
	else:
		f = open(filename,'w') # open the file for writing 
		f.write(text) # write from textview buffer to file
		f.close() # close the writer
		print(filename + " saved.") # notify changed status
		window.set_title(filename) # set new filename to window title

def button_save_as_clicked(self):
	buff = textview.get_buffer() #get textview buffer
	text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True) #get all text from buffer
	dialog = Gtk.FileChooserDialog("Save File As", # get stock save as file dialog
									window,
									 Gtk.FileChooserAction.SAVE,
									 (Gtk.STOCK_CANCEL,
									 Gtk.ResponseType.CANCEL,
									 Gtk.STOCK_SAVE_AS,
									 Gtk.ResponseType.OK))
	response = dialog.run() # open the save as dialog
	if response == Gtk.ResponseType.OK: #if ok is pressed
		f = open(dialog.get_filename(),'w') #save the file using given filename
		f.write(text)
		f.close()
		global filename
		filename = dialog.get_filename() 
		print(filename + " saved.")
	elif response == Gtk.ResponseType.CANCEL:
		print("cancel clicked")
	dialog.destroy()
	window.set_title(filename)

def button_open_clicked(self):
	buff = textview.get_buffer()
	text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True)
	dialog = Gtk.FileChooserDialog("Open File", window, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
	response = dialog.run()
	if response == Gtk.ResponseType.OK:
		f = open(dialog.get_filename(),'r')
		buff.set_text(''.join(f.readlines()))
		global filename
		filename = dialog.get_filename() 
		print(filename + " opened.")
	elif response == Gtk.ResponseType.CANCEL:
		print("cancel clicked")
	dialog.destroy()
	window.set_title(filename)

def on_font_set(self):
	dialog = Gtk.FontChooserDialog("Choose a Font",window)
	response = dialog.run()
	if response == Gtk.ResponseType.OK:
		font_desc = dialog.get_font_desc()
		textview.override_font(font_desc)
		print("new font chosen")
	elif response == Gtk.ResponseType.CANCEL:
		print("cancel clicked")
	dialog.destroy()	

# window
window = Gtk.Window()
window.set_title(filename)
window.resize(500,300)
window.connect("delete-event", Gtk.main_quit)

# box
box = Gtk.Box(orientation="vertical")
window.add(box)

# toolbar
toolbar = Gtk.Toolbar() # create toolbar widget
toolbar.set_style(0) # make toolbar icons only
box.pack_start(toolbar, False, False, 0) # add toolbar to box container

# save toolbar button
button_save = Gtk.ToolButton(icon_name="document-save") # create save button
button_save.connect("clicked", button_save_clicked)
toolbar.insert(button_save, 0) # add save button to toolbar 

# save as toolbar button
button_save_as = Gtk.ToolButton(icon_name="document-save-as") # create save as button
button_save_as.connect("clicked", button_save_as_clicked)
toolbar.insert(button_save_as, 1) # add save as button to toolbar 

# open toolbar button
button_open = Gtk.ToolButton(icon_name="document-open") # create open button
button_open.connect("clicked", button_open_clicked)
toolbar.insert(button_open, 2) # add open button to toolbar 

#font button
button_font = Gtk.ToolButton(icon_name="preferences-desktop-font")
button_font.connect("clicked", on_font_set)
toolbar.insert(button_font, 3)

# textview
scrolled_window = Gtk.ScrolledWindow()
scrolled_window.set_border_width(2)
textview = Gtk.TextView()
scrolled_window.add(textview)
box.pack_start(scrolled_window, True, True, 0)

window.show_all()
Gtk.main()
