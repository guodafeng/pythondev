#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
'''
from checkmono import *
import utility
try:
    import Tkinter as tk
    import tkFont
    import ttk
    from tkFileDialog import askopenfilename, askopenfilenames
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
    from tkinter.filedialog import askopenfilename, askopenfilenames



g_logger = None
def mylogger(path = ''):
    global g_logger
    if g_logger is None:
        g_logger = utility.get_logger(path)

    return g_logger
 
class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, root):
        self.tree = None
        self._root = root
        self._setup_widgets()
        self._build_tree()
        self._item_map = {}
        self._iid_map = {}

    def _setup_widgets(self):
        s = ('Double click row to select base file to compare to.' 
                ' Right click can open check result file.')
        hori = ttk.Frame(self._root)
        hori.pack(side=tk.TOP)
        # info label
        msg = ttk.Label(hori, justify="left", anchor="n",
           padding=(5, 5, 5, 5), text=s)
        msg.pack(side=tk.TOP, fill='both', expand=True)

        # buttons check, add and remove
        chk_btn = ttk.Button(self._root, text='Check added',
                command=self.check_added)
        add_btn = ttk.Button(self._root, text='Add file to check',
                command=self.select_file_to_check)
        del_btn = ttk.Button(self._root, text='Remove selected',
                command=self.remove_selected)
        chk_btn.pack(in_=hori, side=tk.LEFT, padx=20)
        add_btn.pack(in_=hori, side=tk.LEFT, padx=20)
        del_btn.pack(in_=hori, side=tk.LEFT, padx=20)

        container = ttk.Frame(self._root)
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=item_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Create menu
        self.popup = tk.Menu(self._root, tearoff=0)
        self.popup.add_command(label="Remove item",
                command=self.remove_selected)
        self.popup.add_command(label="Open validation result",
                command=self.open_result)
        self.popup.bind('<FocusOut>', self.popup_lose_focus)

        # bind click event
        self.tree.bind('<Double-1>', self.on_dbclick_list)
        self.tree.bind('<Button-3>', self.on_rclick_list)

    def _build_tree(self):
        for col in item_header:
            self.tree.heading(col, text=col.title())
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

    def on_rclick_list(self, event):
            ele = self.tree.identify_row(event.y)
            if ele == '':
                return
            # display the popup menu
            try:
                self.tree.selection_set(ele)
                self.tree.focus(ele)
                self.popup.tk_popup(event.x_root, event.y_root)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.popup.grab_release()

    def popup_lose_focus(self, event = None):
        self.popup.unpost()


    def on_dbclick_list(self, event):
        selected = self.tree.focus()
        mylogger().info(selected)
        if selected in self._iid_map:
            name = askopenfilename(filetypes=[('BDF files', '.bdf')])
            mylogger().info('selected iid = %s, compared to file %s' % \
                    (selected, name))
            if name is not None and name != '':
                self._iid_map[selected][1] = name
                self.tree.item(selected, values = \
                        self._iid_map[selected] )

    def result_file_name(self, checkfile):
        err_file = checkfile[:len(checkfile)-4] + '_check.txt'
        return err_file

    def check_added(self):
        def save_err(errs, checkfile):
            if len(errs) > 0:
                errs = [checkfile + ' has below errors:\n'] + errs 
            else:
                errs = [checkfile + ' passed the check:\n'] 
            utility.save_list(self.result_file_name(checkfile), errs)

        # check added files in treeview
        for iid in self._iid_map:
            check_item = self._iid_map[iid]
            errs = check_bdf(*check_item)
            if len(errs) > 0:
                self.tree.item(iid, tags=('error',))
            else:
                self.tree.item(iid, tags=('passed',))
            save_err(errs, check_item[0])

        self.tree.tag_configure('error', background='red')
        self.tree.tag_configure('passed', background='green')


    def add_check_files(self, items):
        """
        items: [[filename_to_check,base_file]]
        """
        for item in items:
            if item[0] not in self._item_map:
                iid = self.tree.insert('', 'end', values=item)
                self._item_map[item[0]] = iid
                self._iid_map[iid] = item

                # adjust column's width if necessary to fit each value
                for ix, val in enumerate(item):
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(item_header[ix],width=None)<col_w:
                        self.tree.column(item_header[ix], width=col_w)

    def select_file_to_check(self):
        names = askopenfilenames(filetypes=[('BDF files', '.bdf')])
        items = [[name, ''] for name in names]
        self.add_check_files(items)

        mylogger().info(names)


    def open_result(self):
        import webbrowser
        selected = self.tree.focus()
        mylogger().info(selected)
        if selected != '':
            check_item = self._iid_map[selected]
            err_file = self.result_file_name(check_item[0])
            webbrowser.open(err_file)


    def remove_selected(self):
        items = self.tree.selection()
        # update map
        for item in items:
            checkfile = self._iid_map[item][0]
            self._iid_map.pop(item)
            self._item_map.pop(checkfile)
        if len(items) > 0:
            self.tree.delete(items)
   


item_header = ['BDF File to check', 'Base BDF File']

    
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Check conformance of bdf files")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry('%sx%s' % (width//2, height//2))

    MultiColumnListbox(root)
    root.mainloop()



