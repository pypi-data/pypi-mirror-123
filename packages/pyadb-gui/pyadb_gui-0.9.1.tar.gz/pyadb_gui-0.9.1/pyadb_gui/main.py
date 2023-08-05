import subprocess, os, re
import tkinter as tk
from tkinter import ttk
from tkinter.constants import END
import tkinter.messagebox as msg



# frame = ttk.Frame()
 
class HomePage1(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.resizable(0,0)
        self.root.title('pyadb_GUI')
        self.root.geometry('%dx%d' % (400, 300))  # 设置窗口大小

        self.style = ttk.Style()
        self.style.configure('W.TButton', font = ('calibri', 10, 'bold', 'underline'),foreground = 'Green')

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.createPage()
 
    def createPage(self):
        # 页面 1 
        self.btn_page = ttk.Frame(self.notebook, width=380, height=280)
        self.btn_page.pack(fill='both', expand=True)

        # 页面 2
        self.info_page = ttk.Frame(self.notebook, width=380, height=280)
        self.info_page.pack(fill='both', expand=True)

        self.notebook.add(self.btn_page, text='Button')
        self.notebook.add(self.info_page, text='Info')

        # 页面1 布局
        button_press = ButtonPress()

        btn_up = ttk.Button(self.btn_page, text='up',width=12, command=button_press.keyevent_up).grid(row=1, column=2, pady=5)
        btn_down= ttk.Button(self.btn_page, text='down',width=12, command=button_press.keyevent_down).grid(row=3, column=2, pady=5)
        btn_left = ttk.Button(self.btn_page, text='left',width=12, command=button_press.keyevent_left).grid(row=2, column=1, pady=5)
        btn_right = ttk.Button(self.btn_page, text='right',width=12, command=button_press.keyevent_right).grid(row=2, column=3, pady=5)
        btn_enter = ttk.Button(self.btn_page, text='Enter',width=12, command=button_press.keyevent_select).grid(row=2, column=2, pady=5)

        ttk.Button(self.btn_page, text='Back',width=12, command=button_press.keyevent_back).grid(row=4, column=1, pady=5)
        ttk.Button(self.btn_page, text='Home',width=12, command=button_press.keyevent_home).grid(row=4, column=2, pady=5)
        ttk.Button(self.btn_page, text='Menu',width=12, command=button_press.keyevent_menu).grid(row=4, column=3, pady=5)

        ttk.Button(self.btn_page, text='Play/Pause',width=12, command=button_press.keyevent_play).grid(row=5, column=2, pady=5)
        ttk.Button(self.btn_page, text='Volumn_up',width=12, command=button_press.keyevent_vol_up).grid(row=5, column=1, pady=5)
        ttk.Button(self.btn_page, text='Volumn_down',width=12, command=button_press.keyevent_vol_down).grid(row=5, column=3, pady=5)

        short_ble = ttk.Button(self.btn_page, text='Bluetooth',width=12, command=button_press.shortcut_bluetooth, style = 'W.TButton').grid(row=6, column=1, pady=5)
        short_wifi = ttk.Button(self.btn_page, text='Wifi',width=12, command=button_press.shortcut_wifi, style = 'W.TButton').grid(row=6, column=2, pady=5)
        short_mirror = ttk.Button(self.btn_page, text='Mirror',width=12, command=button_press.shortcut_mirror, style = 'W.TButton').grid(row=6, column=3, pady=5)


        input_guide = ttk.Label(self.btn_page, text="input your text:")
        input_guide.grid(column=1, row=7, padx=5, pady=5)

        self.text = tk.StringVar()
        self.text_entry = ttk.Entry(self.btn_page, textvariable=self.text)
        self.text_entry.grid(column=2, row=7)

        ttk.Button(self.btn_page, text="Input", command=button_press.input_text).grid(column=3, row=7)


        # 页面2 布局
        device = DeviceInfo()

        ble_all = device.get_bluetooth_all()

        # tree view 布局
        columns = ('#1', '#2')

        tree = ttk.Treeview(self.info_page, columns=columns, show='headings')

        # define headings
        tree.heading('#1', text='Name')
        tree.heading('#2', text='Value')

        all_device_info = []
        all_device_info.append((f'TV Name', f'{device.get_bluetooth_tv()[0]}'))
        all_device_info.append((f'Time', f'{device.get_time()}'))
        all_device_info.append((f'DSN', f'{device.get_dsn()}'))
        all_device_info.append((f'Version', f'{device.get_build_version()[0]}'))
        all_device_info.append((f'Version2', f'{device.get_build_version()[1]}'))
        all_device_info.append((f'Wifi Mac Address', f'{device.get_mac_addr()[0]}'))
        all_device_info.append((f'Eth Mac Address', f'{device.get_mac_addr()[1]}'))
        all_device_info.append((f'Wifi ip address', f'{device.get_ip_addr()[0]}'))
        all_device_info.append((f'Eth ip address', f'{device.get_ip_addr()[1]}'))

        # all_device_info.append((f'TV ble mac addr', f'{device.get_bluetooth_tv()[1]}'))

        # for i in range(len(ble_all[0])):
        #     all_device_info.append((f'{ble_all[1][i]}', f'{ble_all[0][i]}'))


        # adding data to the treeview
        for item in all_device_info:
            tree.insert('', tk.END, values=item)

        

        # bind the select event
        def item_selected(event):
            for selected_item in tree.selection():
                # dictionary
                item = tree.item(selected_item)
                # list
                record = item['values']

                # copy selected text to clipboard
                # print(f"copied on {record[1]}")
                root.clipboard_clear()
                root.clipboard_append (record[1])

        tree.bind('<Double-1>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.info_page, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')



    def connectPhone(self):
        self.page.destroy()
 
    def sayTry(self):
        msg.showinfo("Message", "手机连接失败,请尝试重新连接")  # 弹出消息窗口

    def sayFail(self):
        msg.showinfo("Message", "手机连接失败，未知错误")  # 弹出消息窗口

    #没有安装adb判断
    def sayNoadb(self):
        msg.showinfo("Message", "没有安装adb或者未配置adb环境变量")  # 弹出消息窗口



class ButtonPress(object):
    def __init__(self):
        pass

    def keyevent_up(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 19')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口
 
    def keyevent_down(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 20')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_left(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 21')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_right(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 22')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_select(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 23')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_back(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 4')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_home(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 3')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_menu(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 82')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_play(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 85')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_vol_up(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 24')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def keyevent_vol_down(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 25')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def shortcut_bluetooth(self):
        subprocess.getstatusoutput('adb shell input keyevent 4')
        out = subprocess.getstatusoutput('adb shell  am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.controllers_bluetooth_devices.ControllersAndBluetoothActivity')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def shortcut_wifi(self):
        subprocess.getstatusoutput('adb shell input keyevent 4')
        out = subprocess.getstatusoutput('adb shell  am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.network.NetworkActivity')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def shortcut_mirror(self):
        out = subprocess.getstatusoutput('adb shell am start -n com.amazon.cast.sink/.DisplayMirroringSinkActivity')
        if out[0]==0:
            pass
        else:
            pass
            # tk.messagebox.showinfo("Message", "失败")  # 弹出消息窗口

    def input_text(self, *args):
        value = str(self.text.get())
        out = subprocess.getstatusoutput(f'adb shell input text {value}')
        self.text_entry.delete(0, END)
        if out[0]==0:
            pass
        else:
            pass

class DeviceInfo(object):
    def __init__(self, dsn = None):
        self.dsn = dsn

    def get_time(self):
        time = os.popen("adb shell date").read().strip()
        return time

    def get_build_version(self):
        info = os.popen("adb shell cat /system/build.prop").read()
        # TODO 多设备识别
        # info = os.popen("adb -s %s shell cat /system/build.prop" % dsn).read()
        info = info.strip()
        try:
            build_info1 = re.findall(r"ro.build.display.id=(.*)", info)[0].strip()
        except:
            build_info1 = None

        try:
            build_info2 = re.findall(r"ro.build.description=(.*)", info)[0].strip()
        except:
            build_info2 = None

        return build_info1, build_info2

    def get_dsn(self):
        info = os.popen("adb shell idme print").read()
        info = info.strip()
        try:
            dsn = re.findall(r"serial:\s(\S*)", info)[0].strip()
        except:
            dsn = None
        return dsn
        
    def get_mac_addr(self):
        info = os.popen("adb shell ifconfig").read()
        info = info.strip()
        try:
            wifi_mac = re.findall(r"wlan0.*HWaddr\s(\S*)", info)[0].strip()
        except:
            wifi_mac = None
        try:
            eth_mac = re.findall(r"eth0.*HWaddr\s(\S*)", info)[0].strip()
        except:
            eth_mac = None

        return wifi_mac, eth_mac

    def get_ip_addr(self):
        info = os.popen("adb shell ifconfig").read()
        info = info.strip()
        try:
            wifi_ip = re.findall(r"wlan0.*\n.*addr:(\S*)", info)[0].strip()
        except:
            wifi_ip = None
        try:
            eth_ip = re.findall(r"eth0.*\n.*addr:(\S*)", info)[0].strip()
        except:
            eth_ip = None
        return wifi_ip, eth_ip

    def get_bluetooth_tv(self):
        info = os.popen("adb shell cat /data/misc/bluedroid/bt_config.conf").read()
        info = info.strip()
        try:
            name = re.findall(r"Name\s=\s(.*)", info)[0].strip()
        except:
            name = None
        try:
            addr = re.findall(r"\[Adapter\][\n]Address\s=\s(.*)", info)[0].strip()
        except:
            addr = None
        return name,addr

    def get_bluetooth_all(self):
        info = os.popen("adb shell cat /data/misc/bluedroid/bt_config.conf").read()
        info = info.strip()
        try:
            device_mac_addr = re.findall(r"\[(\S{17})\]", info)
        except:
            device_mac_addr = None
        try:
            device_name = re.findall(r"Name\s=\s(.*)", info)[1:]
        except:
            device_name = None
        
        # return dict(zip(device_name, device_mac_addr))
        return device_mac_addr, device_name


if __name__ == '__main__':
    root = tk.Tk()
    root.title('pyadb_GUI')
    HomePage1(root)
    root.mainloop()

def main():
    root = tk.Tk()
    root.title('pyadb_GUI')
    
    HomePage1(root)
    root.mainloop()
