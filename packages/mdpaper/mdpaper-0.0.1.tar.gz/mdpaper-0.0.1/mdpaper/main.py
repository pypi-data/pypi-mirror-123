import typer
import subprocess

from typing import Optional
from pathlib import Path
from glob import glob

from mdpaper import settings

from datetime import date

app = typer.Typer()

basecmd = "pandoc"


today = date.today()
    
output_vars = {
    "date": today,
    "y": today.year,
    "m": today.month,
    "d": today.day,
}


@app.callback()
def callback():
    """
    Build a document based on a collection of markdown files.
    """

def _build_args(output, fmt):
    
    args = [settings.pandoc, "-s", "-F", "pandoc-crossref"]
    for pandoc_filter in settings.pandoc_filters:
        args.extend(["-F", pandoc_filter])
    if settings.toc:
        args.append("--toc")
        args.extend(["--toc-depth", settings.toc_depth])
    if settings.references:
        args.extend(["--bibliography", settings.references, "--citeproc"])
    
    files_ = []
    for pattern in settings.index:
        for fp_ in glob(pattern):
            fp = Path(fp_)
            assert fp.is_file(), f"{fp_} does not exist"
            files_.append(str(fp.expanduser().resolve()))

    args.extend(files_)

    if output:
        basename = str(output)
        
    elif settings.output:
        basename = settings.output
    
    output_name = (f"{basename}.{fmt}").format(**output_vars)
    args.extend(["-o", output_name])

    return args, output_name

    

@app.command()
def docx(output: Optional[Path] = typer.Option(default=None, resolve_path=True)):
    """
    Build a .docx document.
    """

    args, output_name = _build_args(output, "docx")

    if settings.template_docx:
        args.extend(["--reference-doc", str(settings.template_docx)])

    # Write to output file
    
    if output:
        basename = str(output)
        
    elif settings.output:
        basename = settings.output

    typer.echo(f"Writing file to {output_name}")

    # typer.echo(args)
    subprocess.run(args)


@app.command()
def pdf(output: Optional[Path] = typer.Option(default=None, resolve_path=True)):
    """
    Build a .pdf document.
    """
    
    args, output_name = _build_args(output, "pdf")
    
    args.extend(["--pdf-engine", settings.pdf_engine])

    typer.echo(f"Writing file to {output_name}")

    # typer.echo(args)
    subprocess.run(args)
