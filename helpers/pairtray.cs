using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;

// Small always-on tray icon for PhoneBox pairing.
// Left-click (or the menu item) opens the Connect Device dialog on the enhanced settings page.
static class PairTray
{
    const string BaseDir = @"C:\Users\Admin\AppData\Local\PhoneBox";
    const string IconPath = BaseDir + @"\phonebox-pair.ico";
    const string ProxyLauncher = BaseDir + @"\pairweb-run.vbs";
    const string ConnectBase = "http://127.0.0.1:8770/#connect-";
    const string SettingsUrl = "http://127.0.0.1:8770/";

    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);

        NotifyIcon tray = new NotifyIcon();
        tray.Icon = File.Exists(IconPath) ? new Icon(IconPath) : SystemIcons.Application;
        tray.Text = "PhoneBox - click to pair a device";
        tray.Visible = true;

        ContextMenuStrip menu = new ContextMenuStrip();
        menu.Items.Add("Pair / Connect Device (QR)", null, (s, e) => OpenConnect());
        menu.Items.Add("Open PhoneBox Settings", null, (s, e) => OpenSettings());
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add("Exit tray icon", null, (s, e) => { tray.Visible = false; Application.Exit(); });
        tray.ContextMenuStrip = menu;

        tray.MouseClick += (s, e) => { if (e.Button == MouseButtons.Left) OpenConnect(); };

        Application.Run();
        tray.Visible = false;
        tray.Dispose();
    }

    static bool ProxyUp()
    {
        try
        {
            using (TcpClient c = new TcpClient())
            {
                c.Connect("127.0.0.1", 8770);
                return true;
            }
        }
        catch { return false; }
    }

    static void EnsureProxy()
    {
        if (ProxyUp()) return;
        try
        {
            ProcessStartInfo si = new ProcessStartInfo();
            si.FileName = @"C:\Windows\System32\wscript.exe";
            si.Arguments = "//B \"" + ProxyLauncher + "\"";
            si.UseShellExecute = false;
            si.CreateNoWindow = true;
            Process.Start(si);
        }
        catch { }
        for (int i = 0; i < 20 && !ProxyUp(); i++) Thread.Sleep(250);
    }

    static void Launch(string url)
    {
        Process.Start(new ProcessStartInfo { FileName = url, UseShellExecute = true });
    }

    static void OpenConnect()
    {
        EnsureProxy();
        // A unique hash makes the page generate a fresh pair of QR codes on every click.
        Launch(ConnectBase + DateTime.UtcNow.Ticks);
    }

    static void OpenSettings()
    {
        EnsureProxy();
        Launch(SettingsUrl);
    }
}
