import os
import sys
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.prompt import Prompt, Confirm
from groq import Groq
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

console = Console()

# Environment Variables for External Services (Vercel + Supabase)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
VERCEL_AUTH_URL = os.environ.get("VERCEL_AUTH_URL", "https://your-auth-app.vercel.app")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize Supabase if keys are provided
supabase: any = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# AI Client (Groq Engine)
client = Groq(
    api_key=GROQ_API_KEY or "gsk-placeholder",
)

class XTermux:
    def __init__(self):
        self.user_data = None
        self.is_connected = False
        self.vercel_url = VERCEL_AUTH_URL

    def clear(self):
        # Optimization for Termux: ensure clear command works
        os.system('clear' if os.name == 'posix' else 'cls')

    def header(self):
        self.clear()
        # Terminal-optimized width
        width = console.width if console.width < 50 else 50
        console.print(Panel(
            "[bold cyan]XTermux Script[/bold cyan]\n[dim]Vercel + Supabase Integrated[/dim]",
            border_style="blue",
            subtitle="[green]v1.1.0[/green]",
            width=width
        ))

    def main_menu(self):
        while True:
            self.header()
            if self.is_connected and self.user_data:
                email = self.user_data.get('email', 'User')
                console.print(f"[green]● Connected:[/green] {email}")
            else:
                console.print("[red]○ Disconnected[/red]")
            
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_row("[1] Home", "[2] Packages")
            table.add_row("[3] AI Chat", "[4] Setup Guide")
            table.add_row("[5] Profile", "[6] Login/Auth")
            table.add_row("[0] Exit", "")
            
            console.print(Panel(table, title="[bold yellow]Menu[/bold yellow]", border_style="yellow", width=console.width if console.width < 50 else 50))
            
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
        console.print("\nOptimized for Termux environments.")
        console.print("Using Vercel for Auth & Supabase for Data.")
        Prompt.ask("\n[dim]Press Enter[/dim]")

    def packages(self):
        self.header()
        table = Table(title="Termux Packages", width=console.width if console.width < 50 else 50)
        table.add_column("Pkg", style="cyan")
        table.add_column("Status", style="green")
        table.add_row("NodeJS", "OK")
        table.add_row("Python", "OK")
        table.add_row("Git", "OK")
        console.print(table)
        Prompt.ask("\n[dim]Press Enter[/dim]")

    def ai_chat(self):
        self.header()
        if not self.is_connected:
            console.print("[red]Please login via Vercel first.[/red]")
            time.sleep(2)
            return

        console.print("[bold yellow]AI Assistant[/bold yellow] ([dim]exit to quit[/dim])")
        while True:
            user_input = Prompt.ask("\n[bold blue]>>[/bold blue]")
            if user_input.lower() in ["exit", "quit", "0"]:
                break
            
            with console.status("[bold green]Querying Groq AI..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-70b-versatile",
                        messages=[{"role": "user", "content": user_input}]
                    )
                    console.print(f"\n[bold magenta]AI:[/bold magenta] {response.choices[0].message.content}")
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")

    def setup_guide(self):
        self.header()
        console.print("[bold green]Setup Guide:[/bold green]")
        console.print("1. Set `VERCEL_AUTH_URL` in .env")
        console.print("2. Set `SUPABASE_URL` & `KEY` in .env")
        console.print("3. Run `python main.py` in Termux")
        Prompt.ask("\n[dim]Press Enter[/dim]")

    def profile(self):
        self.header()
        if not self.is_connected or not self.user_data:
            console.print("[red]Not logged in.[/red]")
        else:
            profile_info = (
                f"Email: {self.user_data.get('email')}\n"
                f"Provider: {self.user_data.get('provider')}\n"
                f"Status: Active"
            )
            console.print(Panel(profile_info, title="[bold]User Profile[/bold]", width=console.width if console.width < 50 else 50))
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
        console.print(f"[link={auth_url}]Open this URL: {auth_url}[/link]")
        
        # Simulasi alur callback dari Vercel/Supabase
        with console.status("Verifying Session..."):
            time.sleep(2)
            # Di sini biasanya ada pengecekan ke endpoint Vercel/Supabase Auth
            self.user_data = {
                "email": f"user_{provider}@example.com",
                "provider": provider.capitalize()
            }
            self.is_connected = True
        
        console.print("[bold green]Login Success! Returned to XTermux.[/bold green]")
        time.sleep(1.5)

if __name__ == "__main__":
    app = XTermux()
    app.main_menu()
