from itertools import count
from pathlib import Path
import glob
import os
import json
import sys

outfile = Path('output.json')

fns = ""

def countFiles(path,extensions):
    files = (p.resolve() for p in Path(path).glob("**/*") if p.suffix in extensions)
    numfiles = 0
    totalSize = 0
    for f in files:
        numfiles+=1
        totalSize += os.path.getsize(f)
    return numfiles, totalSize

def addToRecord(name,count,size,extensions):
    data = ""
    with open(outfile,"r") as f:
        data = json.load(f)
    
    with open(outfile,"w") as f:
        data[name] = {"count":count,"size":size,"ext":", ".join(extensions)}
        json.dump(data,f)

def downloadGithub(name):
    os.system(f"curl -L \"https://github.com/{name}/archive/refs/heads/master.zip\" -o archive.zip && unzip archive.zip > /dev/null && rm archive.zip")

def simpleDirectory(dir,exts,name):
    if not Path(f"{dir}").exists():
        raise RuntimeError(f"Directory {dir} not found, either due to download error or bug")
    fcount, fsize = countFiles(dir,exts)
    os.system(f"rm -rf {name}")
    addToRecord(name,fcount,fsize,exts)

def simpleGithub(account,name,exts,branch="master"):
    downloadGithub(f"{account}/{name}")
    simpleDirectory(f"{name}-{branch}",exts,name)


# ================================= Sizing functions ==========================================


def doRavEngine():
    simpleGithub("Ravbug","RavEngine",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake"})

def doGodot():
    simpleGithub("godotengine","godot",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh"})

def doRust():
    simpleGithub("rust-lang","rust",{".sh",".rs",".rust",".toml"})

def doWebkit():
    simpleGithub("WebKit","WebKit",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl"},"main")

def doUE5():
    simpleGithub("EpicGames","UnrealEngine",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".metal"},"release")

def doLinux():
    os.system("curl \"https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.16.9.tar.xz\" -o archive.xz && unxz -v archive.xz && tar xvf archive > /dev/null")
    simpleDirectory("linux-5.16.9",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".asm", "makefile"}, "linux")

def doLLVM():
    os.system("curl -L \"https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-14.0.0.zip\" -o archive.zip && unzip archive.zip > /dev/null && rm archive.zip")
    simpleDirectory("llvm-project-llvmorg-14.0.0",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".asm", "makefile", ".ll", ".py", "CMakeLists.txt"}, "llvm-project")

def doBlender():
    os.system("git clone https://git.blender.org/blender.git --depth=1")
    simpleDirectory("blender",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".vert",".frag",".vs",".fs",".glsl", ".hlsl", ".vsh",".fsh", ".metal"},"Blender")

def doGCC():
    os.system("git clone git://gcc.gnu.org/git/gcc.git --depth=1")
    simpleDirectory("gcc",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake", ".asm", "makefile", ".ads", ".py", ".go", ".d", ".m", ".mm" ,".s", ".S", ".f90", "CMakeLists.txt"},"gcc")

def doSwift():
    simpleGithub("apple","Swift",{".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".cs", ".in", ".sh", ".cmake",".swift", ".m", ".mm"},"main")


# create output file if it does not exist
if not outfile.exists():
    with open(outfile,"w+") as f:
        outfile.write_text("{}")

def doAll():
    for fn in fns.values():
        fn()

fns = {
    "RavEngine" : doRavEngine,
    "Godot" : doGodot,
    "Rust" : doRust,
    "WebKit" : doWebkit,
    "Unreal" : doUE5,
    "Linux" : doLinux,
    "LLVM" : doLLVM,
    "Blender" : doBlender,
    "gcc" : doGCC,
    "swift" : doSwift,
    "all" : doAll
}
fn = ""
try:
    fn = fns[sys.argv[1]]
except KeyError:
    print(f"{sys.argv[1]}: not a known codebase. Known codebases:")
    for name in fns:
        print(name)
    exit(1)

fn()
