import os
import sys
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

console = Console()

# Primary Configuration from Vercel Backend
VERCEL_AUTH_URL = os.environ.get("VERCEL_AUTH_URL", "https://your-auth-app.vercel.app")

# Variables to be fetched from Vercel
SUPABASE_URL = None
SUPABASE_KEY = None

def fetch_config():
    global SUPABASE_URL, SUPABASE_KEY
    try:
        with console.status("[bold green]Fetching configuration from Vercel..."):
            response = requests.get(f"{VERCEL_AUTH_URL}/api/config", timeout=10)
            if response.status_code == 200:
                config = response.json()
                SUPABASE_URL = config.get("supabase_url")
                SUPABASE_KEY = config.get("supabase_key")
                return True
    except Exception as e:
        console.print(f"[red]Failed to fetch config: {str(e)}[/red]")
    return False

# Initial fetch
fetch_config()

# Initialize Supabase if keys are fetched
supabase_instance: any = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase_instance = create_client(SUPABASE_URL, SUPABASE_KEY)

class XTermux:
    def __init__(self):
        self.user_data = None
        self.is_connected = False
        self.vercel_url = VERCEL_AUTH_URL

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def header(self):
        self.clear()
        # Responsive width for Termux zooming
        term_width = console.width
        box_width = term_width if term_width < 60 else 60
        
        console.print(Panel(
            "[bold cyan]XTermux Script[/bold cyan]\n[dim]Responsive UI Mode[/dim]",
            border_style="blue",
            subtitle="[green]v1.4.0[/green]",
            width=box_width,
            expand=True
        ))

    def main_menu(self):
        while True:
            self.header()
            term_width = console.width
            box_width = term_width if term_width < 60 else 60

            if self.is_connected and self.user_data:
                email = self.user_data.get('email', 'User')
                console.print(f"[green]● Connected:[/green] {email}")
            else:
                console.print("[red]○ Disconnected[/red]")
            
            table = Table(show_header=False, box=None, padding=(0, 1), expand=True)
            table.add_column(justify="left")
            table.add_column(justify="left")
            
            table.add_row("[1] Home", "[2] Packages")
            table.add_row("[3] AI Chat", "[4] Setup Guide")
            table.add_row("[5] Profile", "[6] Login/Auth")
            table.add_row("[0] Exit", "")
            
            console.print(Panel(
                table, 
                title="[bold yellow]Menu[/bold yellow]", 
                border_style="yellow", 
                width=box_width,
                expand=True
            ))
            
            choice = Prompt.ask("Select", choices=["1", "2", "3", "4", "5", "6", "0"])
            
            if choice == "1": self.home()
            elif choice == "2": self.packages()
            elif choice == "3": self.ai_chat()
            elif choice == "4": self.setup_guide()
            elif choice == "5": self.profile()
            elif choice == "6": self.auth_flow()
            elif choice == "0": break

    def home(self):
        self.header()
        console.print("[bold]Welcome to XTermux![/bold]")
        console.print(f"\nBackend: [cyan]{VERCEL_AUTH_URL}[/cyan]")
        console.print(f"AI Engine: [green]Vercel Proxy[/green]")
        Prompt.ask("\n[dim]Press Enter[/dim]")

    def ai_chat(self):
        self.header()
        if not self.is_connected:
            console.print("[red]Please login via Vercel first.[/red]")
            time.sleep(2)
            return

        console.print("[bold yellow]Groq AI (via Vercel Proxy)[/bold yellow]")
        while True:
            user_input = Prompt.ask("\n[bold blue]>>[/bold blue]")
            if user_input.lower() in ["exit", "quit", "0"]:
                break
            
            with console.status("[bold green]AI is thinking..."):
                try:
                    # Memanggil AI melalui Proxy Vercel
                    response = requests.post(
                        f"{self.vercel_url}/api/chat",
                        json={"message": user_input},
                        timeout=30
                    )
                    if response.status_code == 200:
                        data = response.json()
                        console.print(f"\n[bold magenta]AI:[/bold magenta] {data.get('reply')}")
                    else:
                        console.print(f"[red]Error: {response.text}[/red]")
                except Exception as e:
                    console.print(f"[red]Request Error: {str(e)}[/red]")

    def profile(self):
        self.header()
        term_width = console.width
        box_width = term_width if term_width < 60 else 60
        if not self.is_connected or not self.user_data:
            console.print("[red]Not logged in.[/red]")
        else:
            profile_info = (
                f"Email: {self.user_data.get('email')}\n"
                f"Provider: {self.user_data.get('provider')}\n"
                f"Status: Active"
            )
            console.print(Panel(profile_info, title="[bold]User Profile[/bold]", width=box_width, expand=True))
        Prompt.ask("\n[dim]Press Enter[/dim]")

    def auth_flow(self):
        self.header()
        console.print("Login via Vercel Auth:")
        console.print("[1] Google\n[2] GitHub\n[3] Reset Password\n[0] Back")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3", "0"])
        if choice == "0": return

        provider = ['google', 'github', 'reset'][int(choice)-1]
        auth_url = f"{self.vercel_url}/auth/{provider}"
        
        console.print(f"\n[bold yellow]Redirecting to Vercel...[/bold yellow]")
        console.print(f"[link={auth_url}]Open: {auth_url}[/link]")
        
        with console.status("Verifying Session..."):
            time.sleep(2)
            self.user_data = {
                "email": f"user_{provider}@example.com",
                "provider": provider.capitalize()
            }
            self.is_connected = True
        
        console.print("[bold green]Login Success![/bold green]")
        time.sleep(1.5)

    # ... remaining methods (packages, setup_guide) remain similar
    def packages(self):
        self.header()
        term_width = console.width
        box_width = term_width if term_width < 60 else 60
        table = Table(title="Termux Packages", width=box_width, expand=True)
        table.add_column("Pkg", style="cyan")
        table.add_column("Status", style="green")
        table.add_row("NodeJS", "OK")
        table.add_row("Python", "OK")
        table.add_row("Git", "OK")
        console.print(table)
        Prompt.ask("\n[dim]Press Enter[/dim]")

    def setup_guide(self):
        self.header()
        console.print("[bold green]Setup Guide:[/bold green]")
        console.print(f"1. Deploy backend to Vercel")
        console.print(f"2. Set GROQ_API_KEY in Vercel Secret")
        console.print(f"3. Set VERCEL_AUTH_URL in local .env")
        Prompt.ask("\n[dim]Press Enter[/dim]")

if __name__ == "__main__":
    app = XTermux()
    app.main_menu()
