from collections import defaultdict
from os.path import isfile, isdir
from os import listdir, makedirs, remove, removedirs
from glob import glob
import re
import subprocess
import time
from multiprocessing import Process, Queue
from multiprocessing.context import ProcessError
from pathlib import Path
from dolreader.dol import DolFile
from dolreader.section import DataSection, Section, TextSection
from elftools.elf.elffile import ELFFile
from geckolibs.gct import GeckoCodeTable, GeckoCommand

from freighter.constants import *
from freighter.hooks import *


def assert_file_exists(path: str) -> str:
    if isfile(path):
        return path
    raise Exception(f"The file '{path}' does not exist")


def assert_dir_exists(path: str) -> str:
    if isdir(path):
        return path
    raise Exception(f"The folder '{path}' does not exist")


def delete_file(filepath: str) -> bool:
    try:
        remove(filepath)
        return True
    except FileNotFoundError:
        return False


def delete_dir(path: str) -> bool:
    try:
        for file in glob(path + "*", recursive=True):
            delete_file(file)
        removedirs(path)
        return True
    except FileNotFoundError:
        return False


default_source_paths = ["source/", "src/", "code/"]
default_include_paths = ["include/", "includes/", "headers/"]


def get_default_source_dir() -> str:
    for path in default_source_paths:
        if isdir(path):
            return path


def get_default_include_dir() -> list[str]:
    for path in default_include_paths:
        if isdir(path):
            return [path]


def get_dolphin_maps_folder() -> str:
    if PLATFORM == "Windows":
        return str(Path.home()) + "/Documents/Dolphin Emulator/Maps/"
    elif PLATFORM == "Linux":
        return str(Path.home()) + "/.local/share/dolphin-emu/Maps/"
    else:
        print(f"{FYELLOW}[Warning] Could not deduce Dolphin Maps folder.\n{FWHITE}Please set the path with the{FGREEN}add_map_output{FWHITE} method.")
        return str()


class Symbol:
    def __init__(self):
        self.name = ""
        self.demangled_name = ""
        self.section = ""
        self.address = 0
        self.hex_address = 0
        self.size = 0
        self.is_undefined = True
        self.is_weak = False
        self.is_function = False
        self.is_data = False
        self.is_bss = False
        self.is_rodata = False
        self.is_c_linkage = False
        self.is_manually_defined = False
        self.is_written_to_ld = False
        self.source_file = ""
        self.library_file = ""


class Project(object):
    def __init__(self, name: str, gameid: str):
        self.gameid = gameid
        self.project_name = name
        self.verbose = False
        self.sda_base: int = None
        self.sda2_base: int = None
        self.devkitppc = DEVKITPPC
        self.entry_function: str = None
        self.build_dir = "build/"
        self.dol_inpath = "vanilla.dol"
        self.dol_outpath = self.build_dir + "sys/main.dol"
        self.symbols_paths = list[str]()
        self.temp_dir = self.build_dir + "temp/"
        self.linkerscripts = list[str]()
        self.map_inpath: str = None
        self.map_outpaths = [get_dolphin_maps_folder() + self.gameid + ".map"]
        self.linkerscript_template = "template.ld"
        self.base_addresss: int = None
        self.common_args = list[str]()
        self.gcc_args = list[str]()
        self.gpp_args = list[str]()
        self.project_objfile = self.temp_dir + self.project_name + ".o"
        self.ld_args = list[str]()

        self.include_folders = get_default_include_dir()
        self.source_dir = get_default_source_dir()
        self.library_path = "/lib/"
        self.static_libs = list[str]()

        self.c_files = list[str]()
        self.cpp_files = list[str]()
        self.asm_files = list[str]()
        self.object_files = list[str]()
        self.hooks = list[Hook]()

        self.gecko_table = GeckoCodeTable(gameid, name)
        self.symbols = defaultdict(Symbol)
        self.osarena_patcher = None

    def compile(self, input: str, output: str, iscpp=False, queue: Queue = None):
        args = []
        if iscpp:
            args = [self.devkitppc + GPP, "-c"] + self.gpp_args
        else:
            args = [self.devkitppc + GCC, "-c"] + self.gcc_args
        args += self.common_args
        for path in self.include_folders:
            args.append("-I" + path)
        args.extend([input, "-o", output])
        print(f'{COMPILING} "{input}"!')
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode:
            raise ProcessError(f'\n{ERROR} {FWHITE + input}\n{err.decode("utf-8")}\nFailed to compile source. Fix your code.')
        else:
            print(f'{SUCCESS}   "{input}"{FCYAN}')
            if queue:
                queue.put(input)

    def __link(self, outpath):
        print(f"{FLCYAN}Linking...{FYELLOW}")
        args = [self.devkitppc + GPP]
        for arg in self.ld_args:
            args.append("-Wl," + arg)
        for file in self.object_files:
            args.append(file)
        args.extend(self.linkerscripts)
        args.extend(["-Wl,-Map", f"{self.temp_dir + self.project_name}.map"])
        args.extend(["-o", outpath])
        print(args)
        print(f"{FLMAGENTA}")
        exit_code = subprocess.call(args)
        if exit_code:
            raise NameError(f'{ERROR}: failed to link object files"\n')
        else:
            print(f"{LINKED}{FLMAGENTA} -> {FLCYAN}{self.temp_dir + self.project_name}.o")

    def __find_undefined_cpp_symbols(self):
        for file in self.object_files:
            if ".c." in file:
                continue
            self.__analyze_nm((self.dump_nm(file)))

    def __analyze_nm(self, *files: str):
        for file in files:
            print(f"{FYELLOW}Analyzing {FLCYAN+file}...")
            source_file = file.replace(self.temp_dir, "").rsplit(".", 2)[0]
            with open(file, "r") as f:
                for line in f.readlines():
                    if line.startswith(("0", "8")):
                        line = line[8:]
                    (type, symbol_name) = line.strip().split(" ")
                    type = type.lower()
                    symbol = self.symbols[symbol_name]
                    symbol.name = symbol_name
                    if symbol_name.startswith("_Z"):
                        symbol.demangled_name = self.demangle(symbol_name)
                        self.symbols[symbol.demangled_name] = symbol
                    else:
                        symbol.is_c_linkage = True
                        symbol.demangled_name = symbol_name
                    if type == "u":
                        continue
                    if type == "t":
                        symbol.is_function = True
                    elif type == "v":
                        symbol.is_weak = True
                    elif type == "b":
                        symbol.is_bss = True
                    elif type == "d":
                        symbol.is_data = True
                    elif type == "r":
                        symbol.is_rodata = True
                    elif type == "a":
                        symbol.is_manually_defined = True
                    symbol.is_undefined = False
                    if not symbol.source_file:
                        symbol.source_file = source_file
                    else:  # should implement the source object/static lib better
                        symbol.library_file = source_file

    def __generate_linkerscript(self):
        with open(self.temp_dir + self.project_name + "_linkerscript.ld", "w") as f:
            for line in open(self.linkerscript_template, "r").readlines():
                if "$ENTRY" in line:
                    line = "ENTRY(" + self.entry_function + ");\n"
                if "$LIBRARIES" in line:
                    if self.static_libs:
                        for path in self.library_path:
                            f.write(f'SEARCH_DIR("{path}");\n')
                        group = "GROUP("
                        for lib in self.static_libs:
                            group += f'"{lib}",\n\t'
                        group = group[:-3]
                        group += ");\n"
                        f.write(group)
                    continue
                if "$SYMBOLS" in line:
                    line = ""
                    for symbol in self.symbols.values():
                        if symbol.is_manually_defined and not symbol.is_written_to_ld:
                            f.write(f"{symbol.name} = {symbol.hex_address};\n")
                            symbol.is_written_to_ld = True
                if "$START" in line:
                    line = f"\t. = 0x{self.base_addresss:4x};\n"
                    f.write(line)
                    continue
                else:
                    f.write(line)
        self.add_linkerscript(self.temp_dir + self.project_name + "_linkerscript.ld")

    def __analyze_final(self):
        print(f"{FYELLOW}Dumping objdump...{FCYAN}")
        self.dump_objdump(self.project_objfile, "-tSr", "-C")
        self.__analyze_nm((self.dump_nm(self.project_objfile)))
        self.__analyze_readelf(self.dump_readelf(self.project_objfile, "-a", "--wide", "--debug-dump"))

    def __analyze_readelf(self, path: str):
        section_map = {}
        print(f"{FYELLOW}Analyzing {FLCYAN+path}...")
        with open(path, "r") as f:
            while "  [ 0]" not in f.readline():
                pass
            id = 1
            while not (line := f.readline()).startswith("Key"):
                section_map[id] = line[7:].strip().split(" ")[0]
                id += 1
            while "Num" not in f.readline():
                pass
            f.readline()
            while (line := f.readline()) != "\n":
                (num, address, size, type, bind, vis, ndx, *name) = line.split()
                if size == "0":
                    continue
                if name[0] in self.symbols:
                    symbol = self.symbols[name[0]]
                    symbol.hex_address = "0x" + address
                    symbol.address = int(address, 16)
                    symbol.size = int(size)
                    symbol.library_file = self.project_name + ".o"
                    if ndx == "ABS":
                        continue
                    symbol.section = section_map[int(ndx)]

                else:
                    print("cringe" + name[0] + "\n")

    def __load_symbol_defs(self):
        # Load symbols from a file. Supports recognizing demangled c++ symbols
        print(FYELLOW + "Loading manually defined symbols...")
        for file in self.symbols_paths:
            lines = open(file, "r").readlines()
            with open(file + ".cache", "w") as f:
                section = "." + file.split("\\")[1].split(".")[0]
                for line in lines:
                    line = line.rstrip().partition("//")[0]
                    if line:
                        (name, address) = [x.strip() for x in line.split(" = ")]
                        if name in self.symbols:
                            symbol = self.symbols[name]
                            f.write(line + "\n")
                            symbol.hex_address = address
                            symbol.address = int(address, 16)
                            symbol.is_manually_defined = True

    # Need to make this function more resilient against name mangling edgecases
    def get_function_symbol(self, line: str):
        line = re.findall("[A-Za-z0-9_]*\(.*\)", line)[0]
        return re.sub("( *)([*&])([A-Za-z0-9_]*)", r"\2", line)

    def __process_pragmas(self, file_path):
        c_linkage = False
        with open(file_path, "r") as f:
            while line := f.readline():
                line = line.strip()
                if 'extern "C"' in line:
                    c_linkage = True
                if line.startswith("#pragma hook"):
                    line = line[13:].split(" ")
                    type, addresses = line[0], line[1:]
                    while True:  # skip comments and find the next function declaration
                        line = f.readline().strip()
                        if 'extern "C"' in line:
                            c_linkage = True
                        if not line:
                            continue
                        if line[0] == "/":
                            continue
                        elif "(" in line:
                            break
                    func = self.get_function_symbol(line)
                    if c_linkage:
                        func = func.replace("()", "")
                    if type == "bl":
                        for address in addresses:
                            self.hook_branchlink(func, int(address, 16))
                    elif type == "b":
                        for address in addresses:
                            self.hook_branch(func, int(address, 16))
                    else:
                        raise BaseException(f"\n{ERROR} Wrong branch type given in #pragma hook declaration! {FLBLUE}'{type}'{FLRED} is not supported!")
                # elif line.startswith("#pragma write"):
                #    string = line.replace("#pragma write", "")
                #    try:
                #        info = re.findall(r'"([^"]*)"', string)[0]
                #        addresses = re.findall(r"0[xX][0-9a-fA-F]+", string)
                #        addresses.insert(0, info)
                #    except:
                #        raise Exception("In pragma write: function name is not declared in quotes!")
                if c_linkage and "}" in line or ");" in line:
                    c_linkage = False

    def dump_asm(self):
        for item in listdir(self.temp_dir):
            if item.endswith(".o"):
                out = item.split(".")[0] + ".s"
                self.dump_objdump(
                    ["-drsz", f"{self.temp_dir + item}"],
                    f"{self.temp_dir + out}",
                )

    def assert_has_all_the_stuff(self):
        if self.dol_inpath is None:
            print(f"{FYELLOW}[Warning] You didn't specify an input Dol file. You may compile but it won't be injected.\n{FWHITE}Use {FGREEN}set_vanilla_map_file{FWHITE} method.")
        if self.entry_function is None:
            raise Exception(f"{FLRED}You should assign an entry function with C linkage.\n{FWHITE}Use {FGREEN}set_entry_function{FWHITE} method.")
        if self.map_inpath is None:
            print(f"{FYELLOW}[Warning] An input CodeWarrior symbol map was not found for C++Kit to process.\n{FWHITE}Use {FGREEN}set_vanilla_map_file{FWHITE} method.")
        if not self.map_outpaths:
            print(f"{FYELLOW}[Warning] Output path to Dolphin's Maps folder was not found.\n{FWHITE}Use {FGREEN}add_map_output{FWHITE} method.")

    def build(self, dol_inpath=None, dol_outpath=None, verbose=False, clean_up=False):
        self.verbose = verbose
        if dol_inpath is None:
            dol_inpath = self.dol_inpath
        self.assert_has_all_the_stuff()

        if dol_outpath is None:
            dol_outpath = self.dol_outpath

        dol = DolFile(open(dol_inpath, "rb"))

        if self.base_addresss == None:
            self.base_addresss = dol.lastSection.address + dol.lastSection.size
            print(f"{FWHITE}Base address auto-set from ROM end: {FLBLUE}{self.base_addresss:x}\n" f"{FWHITE}Do not rely on this feature if your DOL uses .sbss2\n")
        if self.base_addresss % 32:
            print("WarningING!  DOL sections must be 32-byte aligned for OSResetSystem to work properly!\n")

        makedirs(self.temp_dir, exist_ok=True)

        self.__compile()
        self.__find_undefined_cpp_symbols()
        self.__load_symbol_defs()
        self.__generate_linkerscript()
        self.__link(f"{self.temp_dir + self.project_name}.o")
        self.__process_project()
        self.__analyze_final()
        self.__save_map(f"{self.temp_dir + self.gameid}.map")
        print(f"{FYELLOW}Begin Patching...")
        bin_data = bytearray(open(self.temp_dir + self.project_name + ".bin", "rb").read())
        while (len(bin_data) % 4) != 0:
            bin_data += b"\x00"
        print(f"\n{FGREEN}[{FLGREEN}Gecko Codes{FGREEN}]")
        for gecko_code in self.gecko_table:
            status = f"{FLGREEN}ENABLED {FLBLUE}" if gecko_code.is_enabled() else f"{FLRED}DISABLED{FLYELLOW}"
            if gecko_code.is_enabled() == True:
                for gecko_command in gecko_code:
                    if gecko_command.codetype not in SupportedGeckoCodetypes:
                        status = "OMITTED"

            print("{:12s} ${}".format(status, gecko_code.name))
            if status == "OMITTED":
                print(f"{FLRED}Includes unsupported codetypes:")
                for gecko_command in gecko_code:
                    if gecko_command.codetype not in SupportedGeckoCodetypes:
                        print(gecko_command)

            vaddress = self.base_addresss + len(bin_data)
            geckoblob = bytearray()
            gecko_command_metadata = []

            for gecko_command in gecko_code:
                if gecko_command.codetype == GeckoCommand.Type.ASM_INSERT or gecko_command.codetype == GeckoCommand.Type.ASM_INSERT_XOR:
                    if status == "UNUSED" or status == "OMITTED":
                        gecko_command_metadata.append((0, len(gecko_command.value), status, gecko_command))
                    else:
                        dol.seek(gecko_command._address | 0x80000000)
                        write_branch(dol, vaddress + len(geckoblob))
                        gecko_command_metadata.append(
                            (
                                vaddress + len(geckoblob),
                                len(gecko_command.value),
                                status,
                                gecko_command,
                            )
                        )
                        geckoblob += gecko_command.value[:-4]
                        geckoblob += assemble_branch(
                            vaddress + len(geckoblob),
                            gecko_command._address + 4 | 0x80000000,
                        )
            bin_data += geckoblob
            if gecko_command_metadata:
                self.gecko_code_metadata.append((vaddress, len(geckoblob), status, gecko_code, gecko_command_metadata))
        print("\n")
        self.gecko_table.apply(dol)

        for hook in self.hooks:
            hook.resolve(self.symbols)
            hook.apply_dol(dol)
            if self.verbose:
                print(hook.dump_info())
        print("\n")
        bad_symbols = list[str]()
        for hook in self.hooks:
            if hook.good == False and hook.symbol_name not in bad_symbols:
                bad_symbols.append(hook.symbol_name)
        if bad_symbols:
            badlist = "\n"
            for name in bad_symbols:
                badlist += f'{FLYELLOW}{name}{FLWHITE} found in {FLCYAN}"{self.symbols[name].source_file}"\n'
            raise Exception(
                f"{ERROR} C++Kit could not resolve hook addresses for the given symbols:\n{badlist}\n"
                f"{FLWHITE}Reasons:{FLRED}\n"
                "• The function was optimized out by the compiler for being out of scope of the entry function.\n"
                "• Symbol definitions are missing from C++Kit.\n\n\n"
            )
        if len(bin_data) > 0:
            new_section: Section
            if len(dol.textSections) <= DolFile.MaxTextSections:
                new_section = TextSection(self.base_addresss, bin_data)
            elif len(dol.dataSections) <= DolFile.MaxDataSections:
                new_section = DataSection(self.base_addresss, bin_data)
            else:
                raise RuntimeError("DOL is full!  Cannot allocate any new sections.")
            dol.append_section(new_section)
            self.__patch_osarena_low(dol, self.base_addresss + len(bin_data))

        with open(dol_outpath, "wb") as f:
            dol.save(f)
            del dol

        if clean_up:
            print(f"{FCYAN} Cleaning up temporary files\n")
            delete_dir(self.temp_dir)

        print(f'\n{FLGREEN}🎊 BUILD COMPLETE 🎊\nSaved .dol to {FLCYAN}"{self.dol_outpath}"{FLGREEN}!')

    def __compile(self):
        queue = Queue()
        jobs = list[Process]()

        for source in self.c_files + self.cpp_files:
            outpath = self.temp_dir + source.split("/")[-1] + ".o"
            self.object_files.append(outpath)
            self.__process_pragmas(source)
            task = Process(target=self.compile, args=(source, outpath, source.endswith("cpp")))
            jobs.append(task)
            task.start()

        while any(t.is_alive() for t in jobs):
            pass

    def __process_project(self):
        with open(self.project_objfile, "rb") as f:
            elf = ELFFile(f)
            with open(self.temp_dir + self.project_name + ".bin", "wb") as bin:
                for iter in elf.iter_sections():
                    # Filter out sections without SHF_ALLOC attribute
                    if iter.header["sh_flags"] & 0x2:
                        bin.seek(iter.header["sh_addr"] - self.base_addresss)
                        bin.write(iter.data())

    def __save_map(self, map_path):
        print(f"{FLCYAN}Copying symbols to map...")
        with open(map_path, "w+") as map:
            with open(self.project_objfile, "rb") as f:
                elf = ELFFile(f)
                symtab = elf.get_section_by_name(".symtab")
                new_symbols = []
                for iter in symtab.iter_symbols():
                    # Filter out worthless symbols, as well as STT_SECTION and STT_FILE type symbols.
                    if iter.entry["st_info"]["bind"] == "STB_LOCAL":
                        continue
                    # Symbols defined by the linker script have no section index, and are instead absolute.
                    # Symbols we already have aren't needed in the new symbol map, so they are filtered out.
                    if (iter.entry["st_shndx"] == "SHN_ABS") or (iter.entry["st_shndx"] == "SHN_UNDEF"):
                        continue
                    new_symbols.append(iter)
                new_symbols.sort(key=lambda i: i.entry["st_value"])
                curr_section_name = ""
                for iter in new_symbols:
                    parent_section = elf.get_section(iter.entry["st_shndx"])
                    if curr_section_name != parent_section.name:
                        curr_section_name = parent_section.name
                        # We are better off just setting everything to .text as it allows you to click
                        # on the symbol then right click to copy it's address in Dolphin
                        map.write(f"\n.text section layout\n" "  Starting        Virtual\n" "  address  Size   address\n" "  -----------------------\n".format())
                    map.write(f"  {iter.entry['st_value'] - self.base_addresss:08X} {iter.entry['st_size']:06X} {iter.entry['st_value']:08X}  0 ")
                    if iter.name in self.symbols:
                        symbol = self.symbols[iter.name]
                        map.write(f"{symbol.demangled_name}\t {symbol.section} {symbol.source_file} {symbol.library_file}\n")

                inmap = open(self.map_inpath, "r").readlines()
                map.seek(0)
                map = map.readlines()
                for path in self.map_outpaths:
                    open(path, "w").writelines(inmap + map)

    def demangle(self, string: str):
        process = subprocess.Popen([CPPFLIT, string], stdout=subprocess.PIPE)
        demangled = re.sub("\r\n", "", process.stdout.readline().decode("ascii"))
        if self.verbose:
            print(f" 🧼 {FBLUE+ string + FLMAGENTA} -> {FLGREEN + demangled}")
        return demangled

    def set_symbol_map(self, path: str):
        self.map_inpath = assert_file_exists(path)

    def set_base_address(self, address: int):
        self.base_addresss = address

    def set_devkitppc(self, path: str):
        self.devkitppc = assert_dir_exists(path)

    def set_entry_function(self, func_symbol: str):
        self.entry_function = func_symbol

    def set_sda_bases(self, sda: int, sda2: int):
        self.sda_base = sda
        self.sda2_base = sda2

    def add_map_output(self, path: str):
        self.map_outpaths.append(path)

    def add_linkerscript(self, path: str):
        self.linkerscripts.extend(["-T", assert_file_exists(path)])

    def add_symbols_folder(self, path: str):
        assert_dir_exists(path)
        files = glob(path + "*.txt", recursive=True)
        for file in files:
            self.symbols_paths.append(file)

    def add_include_folder(self, path: str):
        self.include_folders.append(assert_dir_exists(path))

    def add_source_folder(self, path: str):
        assert_dir_exists(path)
        for file in glob(path + "*.cpp"):
            self.add_cpp_file(file.replace("\\", "/"))
        for file in glob(path + "*.c"):
            self.add_c_file(file.replace("\\", "/"))
        for file in glob(path + "*.s"):
            self.add_asm_file(file.replace("\\", "/"))

    def add_gecko_folder(self, path: str):
        assert_dir_exists(path)
        for file in glob(path + "*", recursive=True):
            self.add_gecko_file(file)

    def ignore_cpp_file(self, path: str):
        self.cpp_files.remove(path)

    def ignore_c_file(self, path: str):
        self.cpp_files.remove(path)

    def add_c_file(self, path: str) -> None:
        self.c_files.append(assert_file_exists(path))

    def add_cpp_file(self, path: str):
        self.cpp_files.append(assert_file_exists(path))

    def add_asm_file(self, path: str):
        self.asm_files.append(assert_file_exists(path))

    def add_gecko_file(self, path: str):
        for child in GeckoCodeTable.from_text(open(path, "r").read()):
            self.gecko_table.add_child(child)

    def add_static_library(self, path: str):
        self.static_libs.append(assert_dir_exists(self.library_path + path))

    def hook_branch(self, symbol_name: str, *addresses: int):
        for address in addresses:
            self.hooks.append(BranchHook(address, symbol_name))

    def hook_branchlink(self, symbol_name: str, *addresses: int):
        for address in addresses:
            self.hooks.append(BranchHook(address, symbol_name, lk_bit=True))

    def hook_pointer(self, symbol_name: str, *addresses: int):
        for address in addresses:
            self.hooks.append(PointerHook(address, symbol_name))

    def hook_string(self, address, string, encoding="ascii", max_strlen=None):
        self.hooks.append(StringHook(address, string, encoding, max_strlen))

    def hook_file(self, address, filepath, start=0, end=None, max_size=None):
        self.hooks.append(FileHook(address, filepath, start, end, max_size))

    def hook_immediate16(self, address, symbol_name: str, modifier):
        self.hooks.append(Immediate16Hook(address, symbol_name, modifier))

    def hook_immediate12(self, address, w, i, symbol_name: str, modifier):
        self.hooks.append(Immediate12Hook(address, w, i, symbol_name, modifier))

    def dump_objdump(self, object_path: str, *args: str, outpath: str = None):
        args = [self.devkitppc + OBJDUMP, object_path] + list(args)
        if not outpath:
            outpath = self.temp_dir + object_path.split("/")[-1] + ".objdump"
        with open(outpath, "w") as f:
            subprocess.call(args, stdout=f)
        return outpath

    def dump_nm(self, object_path: str, *args: str, outpath: str = None):
        args = [self.devkitppc + NM, object_path] + list(args)
        if not outpath:
            outpath = self.temp_dir + object_path.split("/")[-1] + ".nm"
        with open(outpath, "w") as f:
            subprocess.call(args, stdout=f)
        return outpath

    def dump_readelf(self, object_path: str, *args: str, outpath: str = None):
        args = [READELF, object_path] + list(args)
        if not outpath:
            outpath = self.temp_dir + object_path.split("/")[-1] + ".readelf"
        with open(outpath, "w") as f:
            subprocess.call(args, stdout=f)
        return outpath

    def __patch_osarena_low(self, dol: DolFile, rom_end: int):
        stack_size = 0x10000
        db_stack_size = 0x2000

        # Stacks are 8 byte aligned
        stack_addr = (rom_end + stack_size + 7 + 0x100) & 0xFFFFFFF8
        stack_end = stack_addr - stack_size
        db_stack_addr = (stack_addr + db_stack_size + 7 + 0x100) & 0xFFFFFFF8
        db_stack_end = db_stack_addr - db_stack_size

        # OSArena is 32 byte aligned
        osarena_lo = (stack_addr + 31) & 0xFFFFFFE0
        db_osarena_lo = (db_stack_addr + 31) & 0xFFFFFFE0

        if self.verbose == True:
            size = rom_end - self.base_addresss
            print(f"{FLCYAN}✨What's new:")
            print(f"{FLBLUE}Mod Size: {FYELLOW}0x{FLYELLOW}{size:x}{FLGREEN} Bytes or {FLYELLOW}{size/1024:.4f}{FLGREEN} KiBs")
            print(f"{FLBLUE}Base Address: {HEX}{self.base_addresss:x}")
            print(f"{FLBLUE}End Address: {HEX}{rom_end:x}")
            print(f"{FLBLUE}Stack Address: {HEX}{stack_addr:x}")
            print(f"{FLBLUE}Stack End Address: {HEX}{stack_end:x}")
            print(f"{FLBLUE}OSArenaLo: {HEX}{osarena_lo:x}")
            print(f"{FLBLUE}Debug Stack Address: {HEX}{db_stack_addr:x}")
            print(f"{FLBLUE}Debug Stack End Address: {HEX}{db_stack_end:x}")
            print(f"{FLBLUE}Debug OSArenaLo: {HEX}{db_osarena_lo:x}")

        # In [__init_registers]...
        dol.seek(0x80005410)
        write_lis(dol, 1, sign_extend(stack_addr >> 16, 16))
        write_ori(dol, 1, 1, stack_addr & 0xFFFF)

        # It can be assumed that the db_stack_addr value is also set somewhere.
        # However, it does not seem to matter, as the DBStack is not allocated.

        # In [OSInit]...
        # OSSetArenaLo( db_osarena_lo );
        dol.seek(0x800EB36C)
        write_lis(dol, 3, sign_extend(db_osarena_lo >> 16, 16))
        write_ori(dol, 3, 3, db_osarena_lo & 0xFFFF)

        # In [OSInit]...
        # If ( BootInfo->0x0030 == 0 ) && ( *BI2DebugFlag < 2 )
        # OSSetArenaLo( _osarena_lo );
        dol.seek(0x800EB3A4)
        write_lis(dol, 3, sign_extend(osarena_lo >> 16, 16))
        write_ori(dol, 3, 3, osarena_lo & 0xFFFF)

        # In [__OSThreadInit]...
        # DefaultThread->0x304 = db_stack_end
        dol.seek(0x800F18BC)
        write_lis(dol, 3, sign_extend(db_stack_end >> 16, 16))
        write_ori(dol, 0, 3, db_stack_end & 0xFFFF)

        # In [__OSThreadInit]...
        # DefaultThread->0x308 = _stack_end
        dol.seek(0x800F18C4)
        write_lis(dol, 3, sign_extend(stack_end >> 16, 16))
        dol.seek(0x800F18CC)
        write_ori(dol, 0, 3, stack_end & 0xFFFF)
