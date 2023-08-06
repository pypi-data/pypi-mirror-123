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
    with ZipFile(archive, 'w') as zip_archive:
        for filename in filenames:
            total_size += os.path.getsize(filename)
            if total_size > max_content_size:
                raise RuntimeError('Too many bytes')

            fileinfo = ZipInfo(str(filename))
            with open(filename, 'rb') as f:
                zip_archive.writestr(fileinfo, f.read(), ZIP_DEFLATED)
    return archive.getbuffer()

def line_entry_mapping(line_program):
    filenames = set()

    # The line program, when decoded, returns a list of line program
    # entries. Each entry contains a state, which we'll use to build
    # a reverse mapping of filename -> #entries.
    lp_entries = line_program.get_entries()
    for lpe in lp_entries:
        # We skip LPEs that don't have an associated file.
        # This can happen if instructions in the compiled binary
        # don't correspond directly to any original source file.
        if not lpe.state or lpe.state.file == 0:
            continue
        filename = lpe_filename(line_program, lpe.state.file)
        filenames.add(filename)

    return filenames

def lpe_filename(line_program, file_index):
    # Retrieving the filename associated with a line program entry
    # involves two levels of indirection: we take the file index from
    # the LPE to grab the file_entry from the line program header,
    # then take the directory index from the file_entry to grab the
    # directory name from the line program header. Finally, we
    # join the (base) filename from the file_entry to the directory
    # name to get the absolute filename.
    lp_header = line_program.header
    file_entries = lp_header["file_entry"]

    # File and directory indices are 1-indexed.
    file_entry = file_entries[file_index - 1]
    dir_index = file_entry["dir_index"]

    # A dir_index of 0 indicates that no absolute directory was recorded during
    # compilation; return just the basename.
    if dir_index == 0:
        return pathlib.Path(os.fsdecode(file_entry.name))

    directory = pathlib.Path(os.fsdecode(lp_header["include_directory"][dir_index - 1]))

    return directory / os.fsdecode(file_entry.name)


@click.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected')
@click.argument('elf_file', type=click.File('rb'))
def debug(ctx, gateway, elf_file):
    try:
        elffile = ELFFile(elf_file)
    except ELFError:
        click.echo('Not an ELF file', err=True)
        ctx.exit(1)

    if not elffile.has_dwarf_info():
        click.echo('ELF file does not have debug info', err=True)
        ctx.exit(1)

    filenames = set()
    dwarfinfo = elffile.get_dwarf_info()
    for cu in dwarfinfo.iter_CUs():
        # Every compilation unit in the DWARF information may or may not
        # have a corresponding line program in .debug_line.
        line_program = dwarfinfo.line_program_for_CU(cu)
        if line_program is None:
            continue

        # Print a reverse mapping of filename -> #entries
        filenames = filenames | line_entry_mapping(line_program)

    archive = zip_files(filenames)
    with open('out.gz', 'wb') as f:
        f.write(archive)
