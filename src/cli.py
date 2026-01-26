"""
Command-line interface for Lesson Summary Agent
"""
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .agent import LessonSummaryAgent
from .config import Config
from .transcript_processor import StudentDatabase

console = Console()


@click.group()
def cli():
    """Lesson Summary Agent - Automate your post-class workflow"""
    pass


@cli.command()
@click.argument('transcript', type=str)
@click.option('--email', '-e', help='Student email address (overrides database)')
@click.option('--draft/--send', default=None, help='Create draft or send email')
@click.option('--sender-name', default='Your Tutor', help='Name to sign email with')
def process(transcript, email, draft, sender_name):
    """
    Process a lesson transcript and send summary email

    TRANSCRIPT can be:
    - Path to transcript file (e.g., ./transcripts/2026-01-05_JohnDoe_Grammar.txt)
    - Fireflies meeting ID
    """
    try:
        agent = LessonSummaryAgent()

        result = agent.process_lesson(
            transcript_source=transcript,
            student_email=email,
            create_draft=draft,
            sender_name=sender_name
        )

        # Show success message
        console.print(Panel.fit(
            f"[green]✓[/green] Successfully processed lesson for [bold]{result['student']}[/bold]\n"
            f"Email: {result['email_status']}",
            title="Success",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.argument('transcript', type=str)
def preview(transcript):
    """
    Preview summary without sending email (for testing)

    TRANSCRIPT can be a file path or Fireflies meeting ID
    """
    try:
        agent = LessonSummaryAgent()
        agent.preview_summary(transcript)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
def setup():
    """
    Interactive setup wizard
    """
    console.print(Panel.fit(
        "Lesson Summary Agent Setup Wizard",
        border_style="blue"
    ))

    config = Config()

    # Check configuration
    console.print("\n[bold]Checking configuration...[/bold]")

    errors = config.validate()

    if errors:
        console.print("\n[yellow]Configuration issues found:[/yellow]")
        for error in errors:
            console.print(f"  • {error}")

        console.print("\n[bold]Setup instructions:[/bold]")
        console.print("1. Copy .env.example to .env and fill in your API keys")
        console.print("2. Download Google OAuth credentials and save as credentials.json")
        console.print("3. Run setup again\n")
        raise click.Abort()

    console.print("[green]✓[/green] Configuration valid")

    # Create directories
    console.print("\n[bold]Creating directories...[/bold]")
    config.setup_directories()
    console.print(f"[green]✓[/green] Transcripts folder: {config.TRANSCRIPTS_FOLDER}")

    # Create sample student database
    if not config.STUDENT_DB_PATH.exists():
        console.print("\n[bold]Creating sample student database...[/bold]")
        db = StudentDatabase()
        db.create_sample_database()
        console.print(f"[green]✓[/green] Created: {config.STUDENT_DB_PATH}")
        console.print("    Edit this file to add your students")

    # Test Google API authentication
    console.print("\n[bold]Testing Google API authentication...[/bold]")
    try:
        from .drive_client import DriveSlideRetriever
        from .gmail_client import GmailSender

        console.print("  Authenticating with Google Drive...")
        drive_client = DriveSlideRetriever()
        console.print("  [green]✓[/green] Drive API connected")

        console.print("  Authenticating with Gmail...")
        gmail_client = GmailSender()
        console.print("  [green]✓[/green] Gmail API connected")

    except Exception as e:
        console.print(f"  [red]✗[/red] Authentication failed: {str(e)}")
        raise click.Abort()

    # Get Drive folder ID (optional)
    if not config.SLIDES_FOLDER_ID:
        console.print("\n[yellow]Note:[/yellow] SLIDES_FOLDER_ID not configured")
        console.print("To enable slide retrieval, add your Google Drive folder ID to .env")

        folder_name = click.prompt("Enter your slides folder name (or press Enter to skip)", default="", show_default=False)

        if folder_name:
            folder_id = drive_client.get_folder_id_by_name(folder_name)
            if folder_id:
                console.print(f"\n[green]Found folder ID:[/green] {folder_id}")
                console.print("Add this to your .env file:")
                console.print(f"SLIDES_FOLDER_ID={folder_id}")
            else:
                console.print(f"[yellow]Could not find folder:[/yellow] {folder_name}")

    console.print("\n[green bold]✓ Setup complete![/green bold]")
    console.print("\nNext steps:")
    console.print("1. Add your students to students.json")
    console.print("2. Place transcript files in the transcripts/ folder")
    console.print("3. Run: lesson-agent process <transcript-file>")


@cli.command()
def list_students():
    """
    List all students in the database
    """
    config = Config()

    if not config.STUDENT_DB_PATH.exists():
        console.print("[yellow]No student database found.[/yellow]")
        console.print("Run: lesson-agent setup")
        return

    import json
    with open(config.STUDENT_DB_PATH, 'r') as f:
        data = json.load(f)

    students = data.get('students', [])

    if not students:
        console.print("[yellow]No students in database.[/yellow]")
        return

    table = Table(title="Student Database")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="green")
    table.add_column("Level", style="yellow")

    for student in students:
        table.add_row(
            student['name'],
            student['email'],
            student.get('level', 'N/A')
        )

    console.print(table)


@cli.command()
@click.option('--folder-id', help='Google Drive folder ID to search')
@click.option('--limit', default=10, help='Number of files to list')
def list_slides(folder_id, limit):
    """
    List recent slide files in Google Drive
    """
    try:
        from .drive_client import DriveSlideRetriever

        drive_client = DriveSlideRetriever()
        files = drive_client.list_recent_files(folder_id=folder_id, limit=limit)

        if not files:
            console.print("[yellow]No files found[/yellow]")
            return

        table = Table(title="Recent Slide Files")
        table.add_column("File Name", style="cyan")
        table.add_column("Modified", style="yellow")
        table.add_column("Link", style="blue")

        for file in files:
            table.add_row(
                file['name'],
                file.get('modifiedTime', 'N/A')[:10],
                file.get('webViewLink', 'N/A')
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")


@cli.command()
def version():
    """Show version information"""
    console.print("[bold]Lesson Summary Agent[/bold]")
    console.print("Version: 1.0.0")
    console.print("AI Model: " + Config.AI_MODEL)


if __name__ == '__main__':
    cli()
