import tkinter
from tkinter import filedialog
import os
import pathlib
from tkinter import scrolledtext
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import ttk
import IO
import Data
import time


class GUI:
    def __init__(self):
        self.master = tkinter.Tk()
        self.master.title("MSRPy - Mass Spec Reduction")
        self.master.geometry('800x450')
        self.source = pathlib.Path(os.getcwd())
        self.destination = None
        self.button_bg = 'white'
        self.button_fg = 'black'
        self.files = []
        self.destination_file=None
        
        ### Build items and placement
        self.label_source = tkinter.Label(self.master, text='Source')
        self.label_source.grid(column=0, row=0, padx=15, pady=5)
        
        self.button_source = tkinter.Button(self.master, text='Select Folder', bg=self.button_bg, fg=self.button_fg, command=self.source_button_action)
        self.button_source.grid(column=1, row=0, padx=15, pady=0)
        
        self.entry_source = tkinter.Entry(self.master, width=100)
        self.entry_source.insert(0, self.source)
        self.entry_source.grid(column=2, row=0, columnspan=5)
        
        self.label_destination = tkinter.Label(self.master, text='Output')
        self.label_destination.grid(column=0, row=1, padx=15, pady=5)
        
        self.button_destination = tkinter.Button(self.master, text='Select Output', bg=self.button_bg, fg=self.button_fg, command=self.destination_button_action)
        self.button_destination.grid(column=1, row=1, padx=15, pady=0)
        
        self.entry_destination = tkinter.Entry(self.master, width=100)
        self.entry_destination.grid(column=2, row=1, columnspan=5)
        
        self.label_files = tkinter.Label(self.master, text="Files Found")
        self.label_files.grid(column=0, row=2)
        
        #self.file_list = scrolledtext.ScrolledText(self.master, undo=True, wrap='none')
        #self.file_list['background'] = self.button_bg
        #self.file_list['foreground'] = self.button_fg
        #self.file_list['font'] = 'Consolas'
        #self.file_list['height'] = 12
        ##self.file_list['ScrollMode'] = 'dynamic'
        #self.file_list.grid(column=0, row=3, columnspan=3)
        
        self.file_list_container = tkinter.Frame(self.master, borderwidth=1, relief='sunken')
        self.file_list = tkinter.Text(self.file_list_container, height=12, wrap='none', borderwidth=0)
        self.file_list_vscroll = tkinter.Scrollbar(self.file_list_container, orient='vertical', command=self.file_list.yview)
        self.file_list_hscroll = tkinter.Scrollbar(self.file_list_container, orient='horizontal', command=self.file_list.xview)
        self.file_list.configure(yscrollcommand=self.file_list_vscroll.set, xscrollcommand=self.file_list_hscroll.set)
        self.file_list.grid(row=0, column=0, sticky='nsew')
        self.file_list_vscroll.grid(row=0, column=1, sticky='ns')
        self.file_list_hscroll.grid(column=0, row=1, sticky='ew')
        self.file_list_container.grid_rowconfigure(0, weight=1)
        self.file_list_container.grid_columnconfigure(0, weight=1)
        self.file_list_container.grid(column = 0, row = 3, columnspan=7)
        
        self.label_file_count = tkinter.Label(self.master, text='{} files.'.format(len(self.files)))
        self.label_file_count.grid(column=5, row=4)
        
        self.label_settings = tkinter.Label(self.master, text='Override Default Settings')
        self.label_settings.grid(column=0, row=4, columnspan=2)
        
        self.label_window = tkinter.Label(self.master, text='Window Size:', justify='right')
        self.label_window.grid(column=0, row=5)
        
        self.spinbox_window = tkinter.Spinbox(self.master, from_=0, to=3, increment=0.1, width=7, justify='left')
        self.spinbox_window.delete(0, tkinter.END)
        self.spinbox_window.insert(0, '0.2')
        self.spinbox_window.grid(column=1, row=5)
        
        self.label_threshold = tkinter.Label(self.master, text='Min Threshold:', justify='right')
        self.label_threshold.grid(column=0, row=6)
        
        self.spinbox_threshold = tkinter.Spinbox(self.master, from_=0, to=400, increment=0.1, width=7, justify='left')
        self.spinbox_threshold.delete(0, tkinter.END)
        self.spinbox_threshold.grid(column=1, row=6)
        self.label_threshold_explain = tkinter.Label(self.master, text='By Default, calculated on a per file basis, average of points that are not peaks.', justify='left')
        self.label_threshold_explain.grid(column=2, row=6, columnspan=3)
        
        self.current_progress_var=tkinter.DoubleVar(0)
        self.style_progress = ttk.Style()
        self.style_progress.theme_use('default')
        self.style_progress.configure('black.Horizontal.TProgressbar', background='green')
        self.progress = Progressbar(self.master, length=300, style='black.Horizontal.TProgressbar', variable=self.current_progress_var, maximum=100)
        self.progress.grid(column=1, row=7, columnspan=3, pady=15)
        
        self.button_run = tkinter.Button(self.master, text="Execute", bg="#d2f9c2", fg=self.button_fg, command=self.execute_button_error_catch)
        self.button_run.grid(column=0, row=7, padx=15, pady=15)
        
        self.master.mainloop()
    
    def destination_button_action(self):
        self.destination_file = filedialog.asksaveasfile(defaultextension='.csv', initialdir=self.source, initialfile='msrpy.out.csv',
                                                    filetypes=[('Comma Separated Values', '.csv'), ('Text File', '.txt')])
        self.destination = pathlib.Path(self.destination_file.name)
        self.destination_file.close()
        self.entry_destination.delete(0, tkinter.END)
        self.entry_destination.insert(0, self.destination)
        self.master.focus()
    
    def source_button_action(self):
        self.source = pathlib.Path(filedialog.askdirectory())
        self.entry_source.delete(0, tkinter.END)
        self.entry_source.insert(0, self.source)
        self.source_directory = IO.Directory(self.source)
        self.files = self.source_directory.recursvieFileTypeSearch('csv')
        self.label_file_count['text']='{} files.'.format(len(self.files))
        for i in self.files:
            self.file_list.insert(tkinter.END, str(i)+'\n')
        self.master.focus()
        
    def execute_button_error_catch(self):
        try:
            self.execute_button_action()
        except Exception as e:
            tkinter.messagebox.showerror('Error Occurred', str(e))
    
    def execute_button_action(self):
        if len(self.files)<1:
            tkinter.messagebox.showwarning("No Source Files", "No Source files were found in selected location.")
        elif self.destination_file is None:
            tkinter.messagebox.showwarning("No Destination File selected", "You have not specified a save location.")
        else:
            self.start = time.time()
            self.window_size=0.2
            self.threshold=None
            try:
                self.window_size=float(self.spinbox_window.get())
            except:
                tkinter.messagebox.showerror('Window Size Error', 'Could not cast Window Size as number')
            try: 
                self.threshold = self.spinbox_threshold.get()
                if self.threshold != '' or len(str(self.threshold))>1:
                    self.threshold = float(self.threshold)
                else:
                    self.threshold=None
            except:
                tkinter.messagebox.showerror('Threshold Error', 'Could not cast Threshold as number')
            self.out_data = []
            self.out_data.append(["Path", "File", "Mass/Charge", "Intensity"])
            self.current_progress=0
            for f in self.files:
                test = IO.CSVFileReader(f)
                test.read()
                data = Data.DataSet(test)
                data.window_max(window_size=float(self.window_size))
                for row in data.max_points:
                    if self.threshold is None and row.y>data.average_non_inflections and row.max_at_x and row.active and row.inflection:
                        self.out_data.append([str(data.path), str(data.name), str(row.x), str(row.y)])
                    elif not self.threshold is None:
                        if row.y>self.threshold and row.max_at_x and row.active and row.inflection:
                            self.out_data.append([str(data.path), str(data.name), str(row.x), str(row.y)])
                self.current_progress+=1
                self.current_progress_var.set((self.current_progress/len(self.files))*100)
                self.master.update_idletasks()
            out = IO.CSVFileWriter(pathlib.Path(self.destination), self.out_data)
            out.write()
            self.stop = time.time()
            tkinter.messagebox.showinfo("Complete!", "Processed {} files, exported {} rows of data, in {:.1f} seconds".format(len(self.files), len(self.out_data)-1, self.stop-self.start))

if __name__ == "__main__":
    GUI()
