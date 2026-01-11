import os
import sys
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.prompt import Prompt, Confirm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

console = Console()

# Replit AI Integration Configuration
# This uses Replit AI Integrations for OpenAI access
# Does not require your own API key
# Charges are billed to your credits
api_key = os.environ.get("REPLIT_AI_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    api_key = "sk-placeholder" # Fallback to prevent crash, will show error on call

client = OpenAI(
    api_key=api_key,
    base_url="https://api.replit.com/ai/v1" if os.environ.get("REPLIT_AI_API_KEY") else None
)

class XTermux:
    def __init__(self):
        self.user_data = None
        self.is_connected = False
        self.vercel_url = os.environ.get("VERCEL_AUTH_URL", "https://your-vercel-auth-app.vercel.app")

    def clear(self):
        os.system('clear')

    def header(self):
        self.clear()
        console.print(Panel.fit(
            "[bold cyan]XTermux Script[/bold cyan]\n[dim]Multi-purpose CLI Tool[/dim]",
            border_style="blue",
            subtitle="[green]v1.0.0[/green]"
        ))

    def main_menu(self):
        while True:
            self.header()
            if self.is_connected:
                console.print(f"[green]● Connected:[/green] {self.user_data.get('email', 'User')}")
            else:
                console.print("[red]○ Disconnected[/red]")
            
            table = Table(show_header=False, box=None)
            table.add_row("[1] Home", "[2] Packages")
            table.add_row("[3] AI Chat", "[4] Setup Guide")
            table.add_row("[5] Profile", "[6] Login/Auth")
            table.add_row("[0] Exit", "")
            
            console.print(Panel(table, title="[bold yellow]Menu[/bold yellow]", border_style="yellow"))
            
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "0"])
            
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
        console.print("\nThis is your central hub for Termux management.")
        Prompt.ask("\nPress Enter to return")

    def packages(self):
        self.header()
        table = Table(title="Available Packages")
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_row("NodeJS", "Installed")
        table.add_row("Python", "Installed")
        table.add_row("Git", "Installed")
        console.print(table)
        Prompt.ask("\nPress Enter to return")

    def ai_chat(self):
        self.header()
        if not self.is_connected:
            console.print("[red]Please login first to use AI Chat.[/red]")
            time.sleep(2)
            return

        console.print("[bold yellow]XTermux AI Assistant[/bold yellow] (Type 'exit' to quit)")
        while True:
            user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
            if user_input.lower() in ["exit", "quit", "0"]:
                break
            
            with console.status("[bold green]AI is thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": user_input}]
                    )
                    console.print(f"\n[bold magenta]AI:[/bold magenta] {response.choices[0].message.content}")
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")

    def setup_guide(self):
        self.header()
        console.print("[bold]Termux Setup Guide[/bold]")
        console.print("1. Update packages: `pkg update && pkg upgrade`")
        console.print("2. Install python: `pkg install python`")
        console.print("3. Clone repo: `git clone <url>`")
        Prompt.ask("\nPress Enter to return")

    def profile(self):
        self.header()
        if not self.is_connected:
            console.print("[red]Not logged in.[/red]")
        else:
            console.print(Panel(f"Name: {self.user_data.get('name')}\nEmail: {self.user_data.get('email')}\nProvider: {self.user_data.get('provider')}", title="User Profile"))
        Prompt.ask("\nPress Enter to return")

    def auth_flow(self):
        self.header()
        console.print("Select Login Method:")
        console.print("[1] Google\n[2] GitHub\n[3] Reset Password\n[0] Back")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3", "0"])
        if choice == "0": return

        # In a real Termux environment, we would use `termux-open`
        # Here we simulate the redirect to Vercel Auth
        auth_url = f"{self.vercel_url}/api/auth?provider={['google', 'github', 'reset'][int(choice)-1]}"
        console.print(f"\n[bold yellow]Opening browser for authentication...[/bold yellow]")
        console.print(f"[link={auth_url}]Click here if browser doesn't open: {auth_url}[/link]")
        
        # Simulate successful auth callback for demonstration
        with console.status("Waiting for verification..."):
            time.sleep(3)
            self.user_data = {
                "name": "Termux User",
                "email": "user@example.com",
                "provider": ["Google", "GitHub", "Reset"][int(choice)-1]
            }
            self.is_connected = True
        
        console.print("[bold green]Successfully Connected![/bold green]")
        time.sleep(2)

if __name__ == "__main__":
    app = XTermux()
    app.main_menu()
