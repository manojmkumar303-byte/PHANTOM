from __future__ import annotations
import base64, json, os, secrets, string, time, tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk
from typing import Any
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

APP_NAME = "PHANTOM Knowledge Vault"
APP_DIR = Path.home() / ".personal_knowledge_vault"
VAULT_PATH = APP_DIR / "vault.pkv"
FORMAT_VERSION = 1
AUTO_LOCK_SECONDS = 300
MIN_PASSWORD_LENGTH = 10
AMBIGUOUS = "O0oIl1|''\""


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def generate_password(length: int = 24, *, uppercase: bool = True, lowercase: bool = True,
                      digits: bool = True, symbols: bool = True, exclude_ambiguous: bool = False) -> str:
    if not isinstance(length, int) or isinstance(length, bool) or not 8 <= length <= 128:
        raise ValueError("Password length must be between 8 and 128.")
    pools = []
    if uppercase: pools.append(string.ascii_uppercase)
    if lowercase: pools.append(string.ascii_lowercase)
    if digits: pools.append(string.digits)
    if symbols: pools.append("!#$%&()*+,-./:;<=>?@[]^_{|}~")
    if exclude_ambiguous:
        pools = ["".join(c for c in pool if c not in AMBIGUOUS) for pool in pools]
    pools = [pool for pool in pools if pool]
    if not pools: raise ValueError("Select at least one character set.")
    if length < len(pools): raise ValueError("Length is too short for the selected character sets.")
    chars = [secrets.choice(pool) for pool in pools]
    alphabet = "".join(pools)
    chars.extend(secrets.choice(alphabet) for _ in range(length - len(chars)))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def read_envelope() -> dict[str, Any] | None:
    if not VAULT_PATH.exists(): return None
    try:
        if VAULT_PATH.stat().st_size > 50 * 1024 * 1024: raise ValueError("Vault file is unexpectedly large.")
        obj = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
        if not isinstance(obj, dict) or obj.get("version") != FORMAT_VERSION:
            raise ValueError("Unsupported or damaged vault format.")
        salt = base64.b64decode(obj.get("salt", ""), validate=True)
        if len(salt) != 16 or not isinstance(obj.get("token"), str) or not obj["token"]:
            raise ValueError("Invalid vault envelope.")
        return obj
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read the vault file: {exc}") from exc


def _write_envelope(envelope: dict[str, Any]) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    try: os.chmod(APP_DIR, 0o700)
    except OSError: pass
    tmp = VAULT_PATH.with_suffix(".tmp")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(envelope, f, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        try: os.chmod(tmp, 0o600)
        except OSError: pass
        os.replace(tmp, VAULT_PATH)
    finally:
        try:
            if tmp.exists(): tmp.unlink()
        except OSError: pass


def create_vault(password: str):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    token = Fernet(key).encrypt(json.dumps({"notes": []}).encode()).decode("ascii")
    envelope = {"version": FORMAT_VERSION, "kdf": "scrypt-n16384-r8-p1",
                "cipher": "Fernet", "salt": base64.b64encode(salt).decode("ascii"), "token": token}
    _write_envelope(envelope)
    return key, [], token


def unlock_vault(password: str, envelope: dict[str, Any]):
    try:
        key = derive_key(password, base64.b64decode(envelope["salt"], validate=True))
        payload = json.loads(Fernet(key).decrypt(envelope["token"].encode("ascii")).decode("utf-8"))
        if not isinstance(payload, dict) or not isinstance(payload.get("notes"), list):
            raise ValueError("Invalid note payload.")
        for note in payload["notes"]:
            if not isinstance(note, dict) or not isinstance(note.get("id"), str):
                raise ValueError("Invalid note record.")
            if any(not isinstance(note.get(k, ""), str) for k in ("title", "content", "category", "updated")):
                raise ValueError("Invalid note fields.")
        return key, payload["notes"], envelope["token"]
    except (InvalidToken, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise PermissionError("Incorrect password or corrupted vault.") from exc


def save_vault(key: bytes, notes: list[dict[str, Any]], expected_token: str) -> str:
    envelope = read_envelope()
    if envelope is None: raise FileNotFoundError("Vault file no longer exists.")
    if not secrets.compare_digest(envelope["token"], expected_token):
        raise RuntimeError("Vault changed outside this application; refusing to overwrite it.")
    envelope["token"] = Fernet(key).encrypt(json.dumps({"notes": notes}, ensure_ascii=False).encode("utf-8")).decode("ascii")
    _write_envelope(envelope)
    return envelope["token"]


class PasswordGenerator(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("PHANTOM Password Generator")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.length = tk.IntVar(value=24)
        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.ambiguous = tk.BooleanVar(value=False)
        self.value = tk.StringVar()
        frame = ttk.Frame(self, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Strong password generator", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))
        row = ttk.Frame(frame); row.pack(fill="x")
        ttk.Label(row, text="Length (8-128)").pack(side="left")
        ttk.Spinbox(row, from_=8, to=128, width=6, textvariable=self.length).pack(side="right")
        for label, var in (("Uppercase", self.upper), ("Lowercase", self.lower), ("Digits", self.digits),
                           ("Symbols", self.symbols), ("Exclude ambiguous characters", self.ambiguous)):
            ttk.Checkbutton(frame, text=label, variable=var).pack(anchor="w")
        ttk.Entry(frame, textvariable=self.value, width=42, font=("Consolas", 11)).pack(fill="x", pady=10)
        buttons = ttk.Frame(frame); buttons.pack(fill="x")
        ttk.Button(buttons, text="Generate", command=self.generate).pack(side="left")
        ttk.Button(buttons, text="Copy", command=self.copy).pack(side="left", padx=6)
        ttk.Button(buttons, text="Close", command=self.close).pack(side="right")
        ttk.Label(frame, text="Generated locally; never saved automatically.").pack(anchor="w", pady=(8, 0))
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.generate()

    def generate(self):
        try:
            self.value.set(generate_password(self.length.get(), uppercase=self.upper.get(), lowercase=self.lower.get(),
                digits=self.digits.get(), symbols=self.symbols.get(), exclude_ambiguous=self.ambiguous.get()))
        except (ValueError, tk.TclError) as exc:
            self.value.set("")
            messagebox.showerror(APP_NAME, str(exc), parent=self)

    def copy(self):
        if not self.value.get():
            messagebox.showinfo(APP_NAME, "Generate a password first.", parent=self); return
        self.clipboard_clear(); self.clipboard_append(self.value.get()); self.update_idletasks()
        messagebox.showinfo(APP_NAME, "Copied to the system clipboard.", parent=self)

    def close(self):
        self.value.set("")
        self.destroy()


class VaultApp:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME); root.geometry("920x620"); root.minsize(760, 500)
        self.key = None; self.notes = []; self.selected_id = None; self.expected_token = None
        self.last_activity = time.monotonic()
        style = ttk.Style(); style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background="#101319"); style.configure("TLabel", background="#101319", foreground="#e8ebf2")
        style.configure("Muted.TLabel", background="#101319", foreground="#9aa4b5")
        style.configure("Heading.TLabel", font=("Segoe UI Semibold", 18), foreground="#f5f7fb")
        style.configure("TButton", padding=(10, 6))
        root.bind_all("<Key>", self.activity); root.bind_all("<Button>", self.activity)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.unlock_screen(); root.after(5000, self.check_lock)

    def activity(self, _event=None):
        if self.key is not None: self.last_activity = time.monotonic()

    def check_lock(self):
        if self.key is not None and time.monotonic() - self.last_activity >= AUTO_LOCK_SECONDS:
            self.lock(); messagebox.showinfo(APP_NAME, "Vault locked after five minutes of inactivity.")
        self.root.after(5000, self.check_lock)

    def clear(self):
        for child in self.root.winfo_children(): child.destroy()

    def unlock_screen(self):
        self.clear(); frame = ttk.Frame(self.root, padding=32); frame.place(relx=.5, rely=.5, anchor="center")
        ttk.Label(frame, text="PHANTOM KNOWLEDGE VAULT", style="Muted.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(frame, text="Your knowledge. Your device.", style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(frame, text="Offline notes protected by a master password.").pack(anchor="w", pady=(0, 18))
        ttk.Label(frame, text="Master password").pack(anchor="w")
        self.password = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=self.password, show="•", width=42); entry.pack(fill="x", pady=8)
        entry.bind("<Return>", lambda _e: self.submit())
        ttk.Button(frame, text="Unlock vault", command=self.submit).pack(fill="x")
        if not VAULT_PATH.exists(): ttk.Label(frame, text="First launch: choose a master password (10+ characters).").pack(anchor="w", pady=10)
        entry.focus_set()

    def submit(self):
        password = self.password.get()
        if not password: messagebox.showerror(APP_NAME, "Enter a master password."); return
        try:
            envelope = read_envelope()
            if envelope is None:
                if len(password) < MIN_PASSWORD_LENGTH:
                    messagebox.showerror(APP_NAME, "Choose at least 10 characters."); return
                confirm = simpledialog.askstring(APP_NAME, "Confirm master password:", show="•", parent=self.root)
                if confirm is None: self.password.set(""); return
                if confirm != password:
                    self.password.set(""); messagebox.showerror(APP_NAME, "Passwords do not match."); return
                self.key, self.notes, self.expected_token = create_vault(password)
            else:
                self.key, self.notes, self.expected_token = unlock_vault(password, envelope)
            self.password.set(""); self.last_activity = time.monotonic(); self.main_screen()
        except Exception as exc:
            self.password.set("")
            messagebox.showerror(APP_NAME, "Could not unlock vault. Check the password and vault file.\n" + str(exc))

    def main_screen(self):
        self.clear(); outer = ttk.Frame(self.root, padding=18); outer.pack(fill="both", expand=True)
        header = ttk.Frame(outer); header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="Knowledge Vault", style="Heading.TLabel").pack(side="left")
        ttk.Button(header, text="Password Generator", command=lambda: PasswordGenerator(self.root)).pack(side="right", padx=6)
        ttk.Button(header, text="Lock", command=self.lock).pack(side="right")
        body = ttk.Frame(outer); body.pack(fill="both", expand=True)
        left = ttk.Frame(body, padding=10); left.pack(side="left", fill="y", padx=(0, 12))
        ttk.Label(left, text="YOUR NOTES").pack(anchor="w")
        self.search = tk.StringVar(); ttk.Entry(left, textvariable=self.search, width=26).pack(fill="x", pady=6)
        self.search.trace_add("write", lambda *_: self.refresh())
        ttk.Button(left, text="+ New note", command=self.new_note).pack(fill="x", pady=(0, 6))
        self.tree = ttk.Treeview(left, columns=("category",), show="tree headings", height=17)
        self.tree.heading("#0", text="Title"); self.tree.heading("category", text="Category")
        self.tree.column("#0", width=160); self.tree.column("category", width=90)
        self.tree.pack(fill="both", expand=True); self.tree.bind("<<TreeviewSelect>>", self.select)
        right = ttk.Frame(body); right.pack(side="left", fill="both", expand=True)
        self.title = tk.StringVar(); ttk.Entry(right, textvariable=self.title, font=("Segoe UI", 14)).pack(fill="x", pady=(0, 6))
        self.category = tk.StringVar(value="General")
        ttk.Combobox(right, textvariable=self.category, values=("General", "Study", "Code", "Research", "Ideas", "Personal")).pack(fill="x", pady=(0, 6))
        self.content = tk.Text(right, wrap="word", undo=True); self.content.pack(fill="both", expand=True, pady=(0, 8))
        row = ttk.Frame(right); row.pack(fill="x")
        ttk.Button(row, text="Save note", command=self.save_note).pack(side="left")
        ttk.Button(row, text="Delete", command=self.delete_note).pack(side="left", padx=6)
        self.status = tk.StringVar(value="Unlocked. Notes are encrypted on disk.")
        ttk.Label(right, textvariable=self.status, style="Muted.TLabel").pack(anchor="w", pady=8)
        self.refresh(); self.clear_editor()

    def clear_editor(self):
        self.selected_id = None; self.title.set(""); self.category.set("General"); self.content.delete("1.0", "end")
        if hasattr(self, "tree"): self.tree.selection_remove(self.tree.selection())

    def refresh(self):
        if not hasattr(self, "tree"): return
        q = self.search.get().strip().casefold()
        for item in self.tree.get_children(): self.tree.delete(item)
        for note in sorted(self.notes, key=lambda n: n.get("updated", ""), reverse=True):
            hay = " ".join(str(note.get(k, "")) for k in ("title", "category", "content")).casefold()
            if q and q not in hay: continue
            self.tree.insert("", "end", iid=note["id"], text=note.get("title") or "(Untitled)", values=(note.get("category", "General"),))

    def select(self, _event=None):
        sel = self.tree.selection()
        if not sel: return
        note = next((n for n in self.notes if n["id"] == sel[0]), None)
        if note is None: return
        self.selected_id = note["id"]; self.title.set(note.get("title", "")); self.category.set(note.get("category", "General"))
        self.content.delete("1.0", "end"); self.content.insert("1.0", note.get("content", ""))
        self.status.set("Selected note.")

    def new_note(self):
        self.clear_editor(); self.content.focus_set(); self.status.set("New note. Save when ready.")

    def persist(self, candidate):
        try:
            token = save_vault(self.key, candidate, self.expected_token)
        except Exception as exc:
            messagebox.showerror(APP_NAME, "Could not save the vault. Your previous saved data was preserved.\n" + str(exc)); return False
        self.notes = candidate; self.expected_token = token; return True

    def save_note(self):
        if self.key is None: return
        title = self.title.get().strip(); content = self.content.get("1.0", "end-1c")
        category = self.category.get().strip() or "General"
        if not title and not content.strip():
            messagebox.showinfo(APP_NAME, "Add a title or some content first."); return
        now = time.strftime("%Y-%m-%d %H:%M"); candidate = [dict(n) for n in self.notes]
        if self.selected_id:
            note = next((n for n in candidate if n["id"] == self.selected_id), None)
        else: note = None
        if note is None:
            note = {"id": secrets.token_hex(8)}; candidate.append(note)
        note.update(title=title or "Untitled", content=content, category=category, updated=now)
        if not self.persist(candidate): return
        self.selected_id = note["id"]; self.refresh()
        if self.selected_id in self.tree.get_children(): self.tree.selection_set(self.selected_id)
        self.status.set("Saved locally.")

    def delete_note(self):
        if not self.selected_id: messagebox.showinfo(APP_NAME, "Select a note first."); return
        if not messagebox.askyesno(APP_NAME, "Delete this note permanently?"): return
        candidate = [dict(n) for n in self.notes if n["id"] != self.selected_id]
        if self.persist(candidate): self.refresh(); self.clear_editor(); self.status.set("Note deleted.")

    def lock(self):
        self.key = None; self.notes = []; self.expected_token = None; self.selected_id = None
        self.unlock_screen()

    def close(self):
        self.key = None; self.notes = []; self.expected_token = None; self.root.destroy()


def main():
    root = tk.Tk()
    VaultApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
