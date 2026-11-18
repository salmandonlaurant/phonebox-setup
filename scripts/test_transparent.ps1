Add-Type @"
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Threading;

public static class Tw {
  delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc p, IntPtr l);
  [DllImport("user32.dll")] static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
  [DllImport("user32.dll", EntryPoint="GetWindowLongPtrW")] static extern IntPtr GetWindowLongPtr(IntPtr h, int idx);
  [DllImport("user32.dll", EntryPoint="SetWindowLongPtrW")] static extern IntPtr SetWindowLongPtr(IntPtr h, int idx, IntPtr val);
  [DllImport("user32.dll")] static extern bool SetLayeredWindowAttributes(IntPtr h, uint cr, byte alpha, uint flags);

  static readonly HashSet<IntPtr> Existing = new HashSet<IntPtr>();
  static readonly Dictionary<uint,string> Names = new Dictionary<uint,string>();
  static volatile bool running = false;
  static Thread worker;

  static string Pn(uint pid){ string n; if(Names.TryGetValue(pid,out n)) return n; try{n=System.Diagnostics.Process.GetProcessById((int)pid).ProcessName;}catch{n="";} Names[pid]=n; return n; }

  public static void Start(){
    Existing.Clear();
    EnumWindows((h,l)=>{uint p;GetWindowThreadProcessId(h,out p);if(Pn(p)=="brave")Existing.Add(h);return true;},IntPtr.Zero);
    running=true; worker=new Thread(Loop); worker.IsBackground=true; worker.Start();
  }
  public static void Stop(){running=false;if(worker!=null)worker.Join(1000);}
  public static void CloseOld(){
    EnumWindows((h,l)=>{uint p;GetWindowThreadProcessId(h,out p);
      if(Pn(p)=="brave"){var s=new StringBuilder(512);GetWindowText(h,s,512);
        if(s.ToString().IndexOf("YouTube Music",StringComparison.OrdinalIgnoreCase)>=0) PostMessage(h,0x0010,IntPtr.Zero,IntPtr.Zero);}
      return true;},IntPtr.Zero);
  }
  static void Loop(){
    while(running){
      EnumWindows((h,l)=>{
        if(Existing.Contains(h))return true;
        uint p;GetWindowThreadProcessId(h,out p);
        if(Pn(p)=="brave"){
          var s=new StringBuilder(512);GetWindowText(h,s,512);
          if(s.Length>0){
            IntPtr ex=GetWindowLongPtr(h,-20);
            long v=ex.ToInt64() | 0x00080000L; // WS_EX_LAYERED
            SetWindowLongPtr(h,-20,new IntPtr(v));
            SetLayeredWindowAttributes(h,0,0,0x2); // LWA_ALPHA, alpha 0
          }
        }
        return true;},IntPtr.Zero);
      Thread.Sleep(5);
    }
  }
}
"@
[Tw]::CloseOld()
Start-Sleep -Milliseconds 900
[Tw]::Start()
Start-Process -FilePath 'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe' -ArgumentList @('--app=https://music.youtube.com/watch?v=6gRbAU4Puek')
Start-Sleep -Seconds 5
[Tw]::Stop()
