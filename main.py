import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

console = Console()

# Configuration (Direct Groq AI)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize Groq Client
client = None
if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        console.print(f"[red]Error initializing Groq: {e}[/red]")

class XTermux:
    def __init__(self):
        self.version = "2.0.0"

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def header(self):
        self.clear()
        term_width = console.width
        box_width = term_width if term_width < 60 else 60
        
        console.print(Panel(
            f"[bold cyan]XTermux Script[/bold cyan]\n[dim]Stand-alone AI Mode[/dim]",
            border_style="blue",
            subtitle=f"[green]v{self.version}[/green]",
            width=box_width,
            expand=True
        ))

    def main_menu(self):
        while True:
            self.header()
            term_width = console.width
            box_width = term_width if term_width < 60 else 60

            console.print("[green]● Mode: No Login (Public)[/green]")
            
            table = Table(show_header=False, box=None, padding=(0, 1), expand=True)
            table.add_column(justify="left")
            table.add_column(justify="left")
            
            table.add_row("[1] Home", "[2] Packages")
            table.add_row("[3] AI Chat", "[4] Setup Guide")
            table.add_row("[0] Exit", "")
            
            console.print(Panel(
                table, 
                title="[bold yellow]Menu[/bold yellow]", 
                border_style="yellow", 
                width=box_width,
                expand=True
            ))
            
            choice = Prompt.ask("Select", choices=["1", "2", "3", "4", "0"])
            
            if choice == "1": self.home()
            elif choice == "2": self.packages()
            elif choice == "3": self.ai_chat()
            elif choice == "4": self.setup_guide()
            elif choice == "0": break

    def home(self):
        self.header()
        console.print("[bold]Welcome to XTermux![/bold]")
        console.print("\nThis version is now standalone. No login required.")
        console.print(f"AI Engine: [green]Groq Llama-3.1[/green]")
        Prompt.ask("\n[dim]Press Enter[/dim]")

    def ai_chat(self):
        self.header()
        if not client:
            console.print("[red]GROQ_API_KEY not found in .env![/red]")
            Prompt.ask("\n[dim]Press Enter[/dim]")
            return

        console.print("[bold yellow]Groq AI Chat[/bold yellow] ([dim]type 'exit' to quit[/dim])")
        while True:
            user_input = Prompt.ask("\n[bold blue]>>[/bold blue]")
            if user_input.lower() in ["exit", "quit", "0"]:
                break
            
            with console.status("[bold green]Thinking..."):
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.1-70b-versatile",
                        messages=[{"role": "user", "content": user_input}]
                    )
                    console.print(f"\n[bold magenta]AI:[/bold magenta] {completion.choices[0].message.content}")
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")

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
        console.print("1. Get API Key from [bold]console.groq.com[/bold]")
        console.print("2. Set [bold]GROQ_API_KEY[/bold] in .env")
        console.print("3. Run: [bold]python main.py[/bold]")
        Prompt.ask("\n[dim]Press Enter[/dim]")

if __name__ == "__main__":
    app = XTermux()
    app.main_menu()
