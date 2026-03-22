# Free Teradata Database Setup on Windows WSL2

Teradata provides a free **Vantage Express** VM image that runs on VirtualBox. Under WSL2, you run VirtualBox inside Windows, then connect to the VM from WSL2.

---

## Prerequisites

- Windows 10/11 with WSL2 enabled
- VirtualBox installed on Windows (not inside WSL2)
- ~40 GB free disk space

---

## Steps

### 1. Download Vantage Express

1. Create a free account at <https://downloads.teradata.com/>.
2. Download **Vantage Express** (the VirtualBox `.ova` file, ~25 GB).

### 2. Import the VM into VirtualBox (Windows side)

```powershell
# In a Windows terminal (PowerShell or CMD)
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" import VantageExpress.ova
```

Or use the VirtualBox GUI: **File → Import Appliance**.

### 3. Start the VM

```powershell
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "Vantage 17.20" --type headless
```

The database is ready when startup completes (allow ~3–5 minutes).

### 4. Find the VM IP

```powershell
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" guestproperty get "Vantage 17.20" /VirtualBox/GuestInfo/Net/0/V4/IP
```

Alternatively, open the VM console and run `ifconfig` inside it.

The default host-only IP is typically `192.168.56.101`.

### 5. Connect from WSL2

Install the Python driver inside WSL2:

```bash
pip install teradatasql teradataml sqlalchemy-teradata
```

Test connectivity:

```python
import teradatasql

con = teradatasql.connect(
    host="192.168.56.101",  # VM IP from step 4
    user="dbc",
    password="dbc",
)
cur = con.cursor()
cur.execute("SELECT CURRENT_DATE")
print(cur.fetchone())
con.close()
```

Default credentials: **user** `dbc` / **password** `dbc`.

---

## Tips

| Topic | Detail |
|---|---|
| Port | Teradata listens on **1025** (TCP). Ensure VirtualBox network allows it. |
| Network adapter | Use **Host-Only Adapter** in VirtualBox so Windows and WSL2 can both reach the VM. |
| WSL2 host IP | From WSL2, the Windows host is reachable at the IP shown by `cat /etc/resolv.conf` (nameserver line). |
| Stopping the VM | `VBoxManage controlvm "Vantage 17.20" poweroff` |
| Docs | <https://quickstarts.teradata.com/vantage.express.vmware.html> |

---

## Environment Variables (optional)

Set these in `~/.bashrc` or `~/.profile` to avoid hard-coding credentials:

```bash
export TERADATA_HOST=192.168.56.101
export TERADATA_USER=dbc
export TERADATA_PASSWORD=dbc
export TERADATA_DATABASE=DBC
```
