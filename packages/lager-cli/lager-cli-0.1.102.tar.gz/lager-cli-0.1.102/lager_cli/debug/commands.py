"""
    lager.debug.commands

    Debug an elf file
"""
import pathlib
import os
from io import BytesIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import click
from ..context import get_default_gateway
from ..elftools.elf.elffile import ELFFile
from ..elftools.common.exceptions import ELFError

def zip_files(filenames, max_content_size=10_000_000):
    """
        Zip a set of files
    """
    archive = BytesIO()
    total_size = 0
    cwd = pathlib.Path.cwd()
    with ZipFile(archive, 'w') as zip_archive:
        for filename in filenames:
            total_size += os.path.getsize(filename)

            resolved = filename.resolve().relative_to(cwd)
            fileinfo = ZipInfo(str(resolved))
            with open(filename, 'rb') as f:
                zip_archive.writestr(fileinfo, f.read(), ZIP_DEFLATED)
    return archive.getbuffer()

def line_entry_mapping(top_die, line_program):
    """
    The line program, when decoded, returns a list of line program
    entries. Each entry contains a state, which we'll use to build
    a reverse mapping of filename -> #entries.
    """

    filenames = set()

    lp_entries = line_program.get_entries()
    comp_dir = top_die.attributes.get('DW_AT_comp_dir', None)
    if comp_dir:
        comp_dir = os.fsdecode(comp_dir.value)

    for lpe in lp_entries:
        # We skip LPEs that don't have an associated file.
        # This can happen if instructions in the compiled binary
        # don't correspond directly to any original source file.
        if not lpe.state or lpe.state.file == 0:
            continue
        filename = lpe_filename(filenames, comp_dir, line_program, lpe.state.file)
        if filename is not None:
            filenames.add(filename)

    return filenames

def lpe_filename(filenames, comp_dir, line_program, file_index):
    """
    Retrieving the filename associated with a line program entry
    involves two levels of indirection: we take the file index from
    the LPE to grab the file_entry from the line program header,
    then take the directory index from the file_entry to grab the
    directory name from the line program header. Finally, we
    join the (base) filename from the file_entry to the directory
    name to get the absolute filename.
    """
    lp_header = line_program.header
    file_entries = lp_header["file_entry"]

    # File and directory indices are 1-indexed.
    file_entry = file_entries[file_index - 1]
    dir_index = file_entry["dir_index"]

    # A dir_index of 0 indicates that no absolute directory was recorded during
    # compilation; return just the basename.
    if dir_index == 0:
        basepath = pathlib.Path(os.fsdecode(file_entry.name))
    else:
        directory = pathlib.Path(os.fsdecode(lp_header["include_directory"][dir_index - 1]))
        basepath = directory / os.fsdecode(file_entry.name)

    if comp_dir:
        full_candidate = comp_dir / basepath
        if full_candidate in filenames:
            return None
        if full_candidate.exists():
            return full_candidate

    return basepath


@click.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected')
@click.argument('elf_file', type=click.Path(exists=True))
def debug(ctx, gateway, elf_file):
    """
        Debug a DUT using an ELF file
    """
    try:
        elffile = ELFFile(open(elf_file, 'rb'))
    except ELFError:
        click.echo(f'Error: \'{elf_file}\' is not an ELF file', err=True)
        ctx.exit(1)

    if not elffile.has_dwarf_info():
        click.echo(f'Error: \'{elf_file}\' does not have debug info', err=True)
        ctx.exit(1)

    filenames = {pathlib.Path(elf_file)}
    dwarfinfo = elffile.get_dwarf_info()
    for cu in dwarfinfo.iter_CUs():
        # Every compilation unit in the DWARF information may or may not
        # have a corresponding line program in .debug_line.
        line_program = dwarfinfo.line_program_for_CU(cu)
        if line_program is None:
            continue

        top_die = cu.get_top_DIE()

        # Print a reverse mapping of filename -> #entries
        filenames = filenames | line_entry_mapping(top_die, line_program)

    archive = zip_files(filenames)
    _ = archive
