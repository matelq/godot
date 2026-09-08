#!/usr/bin/env python3
"""Integration test for the fork's multi-assembly C# script support.

Builds a Godot project whose [GlobalClass] types come from referenced
assemblies — one direct NuGet reference, one transitive, one in-tree project —
and asserts that the source generator stamped each type with the right script
path.

Assembly-backed types must get "csharp://<assembly>/<Namespace>.<Type>.cs";
types whose sources live under the project keep ordinary "res://" paths.
Upstream's generator emits "res://../X.cs" for the assembly-backed case, which
the editor then fails to open at load time — that regression is what this test
exists to catch, and it is why the fork must never resolve Godot.SourceGenerators
to upstream's package.

Unlike Godot.SourceGenerators.Tests, which drives the generator directly, this
exercises the packaged SDK: NuGet packing, the Sdk.props/targets wiring and
transitive package references all have to be correct for it to pass.

Usage:
    python verify.py [--version <fork package version>]
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixture"
FEED = HERE / ".feed"
OUTPUT = FIXTURE / ".godot" / "mono" / "temp" / "bin" / "Debug"

# assembly -> {type: expected script path}
EXPECTED = {
    "ExternalModule": {
        "InventorySystem": "csharp://ExternalModule/ExternalModule.InventorySystem.cs",
        # A Resource, not a Node: the case pcloves reported on #117452.
        "InventoryItem": "csharp://ExternalModule/ExternalModule.InventoryItem.cs",
    },
    "TransitiveModule": {
        "QuestTracker": "csharp://TransitiveModule/TransitiveModule.QuestTracker.cs",
    },
    "InTreeModule": {
        "HealthComponent": "res://InTreeModule/HealthComponent.cs",
    },
}


def run(cmd):
    print(f"+ {' '.join(str(c) for c in cmd)}", flush=True)
    subprocess.run(cmd, check=True)


def detect_version():
    for nupkg in FEED.glob("*.nupkg"):
        m = re.fullmatch(r"cracktower\.godot\.sharp\.(.+)\.nupkg", nupkg.name, re.IGNORECASE)
        if m:
            return m.group(1)
    sys.exit(f"No CrackTower.Godot.Sharp package in {FEED} — nothing to test against.")


def prepare(version):
    (FIXTURE / "global.json").write_text(
        '{\n  "msbuild-sdks": {\n    "CrackTower.Godot.NET.Sdk": "%s"\n  }\n}\n' % version
    )
    # Same-version packages left in the cache would shadow a fresh build.
    cache = Path.home() / ".nuget" / "packages"
    for name in ("cracktower.godot.net.sdk", "cracktower.godot.sharp",
                 "cracktower.godot.sharpeditor", "cracktower.godot.sourcegenerators",
                 "externalmodule", "transitivemodule"):
        shutil.rmtree(cache / name, ignore_errors=True)
    shutil.rmtree(FIXTURE / ".godot", ignore_errors=True)
    for stale in FEED.glob("ExternalModule.*.nupkg"):
        stale.unlink()
    for stale in FEED.glob("TransitiveModule.*.nupkg"):
        stale.unlink()


def build(version):
    prop = f"-p:GodotForkVersion={version}"
    # TransitiveModule first: ExternalModule consumes it as a package, so it has
    # to be in the feed before ExternalModule restores.
    for module in ("TransitiveModule", "ExternalModule"):
        run(["dotnet", "pack", str(HERE / "external" / module / f"{module}.csproj"),
             "-c", "Release", "-o", str(FEED), prop])
    run(["dotnet", "build", str(FIXTURE / "MainProject" / "MainProject.csproj"), prop])


def check_paths():
    """Assert the ScriptPath attribute baked into each built assembly.

    The attribute argument lands in the metadata heap as plain UTF-8, so a byte
    search is enough and avoids needing a metadata reader here.
    """
    ok = True
    for assembly, types in EXPECTED.items():
        dll = OUTPUT / f"{assembly}.dll"
        if not dll.is_file():
            print(f"  FAIL {assembly}.dll was not built to {OUTPUT}")
            ok = False
            continue
        blob = dll.read_bytes()
        for type_name, want in types.items():
            if want.encode() in blob:
                print(f"  PASS {assembly}.{type_name}: {want}")
            else:
                found = re.findall(rb"(?:csharp|res)://[\w./-]*" + type_name.encode() + rb"\.cs", blob)
                actual = found[0].decode() if found else "no script path at all"
                print(f"  FAIL {assembly}.{type_name}: got {actual}, expected {want}")
                ok = False
    return ok


def check_no_broken_paths():
    """No assembly may reference a source file outside the project root.

    "res://../X.cs" is what upstream's generator produces for assembly-backed
    scripts; the path escapes res:// and the editor cannot open it.
    """
    ok = True
    for dll in OUTPUT.glob("*.dll"):
        for bad in re.findall(rb"res://\.\./[\w./-]*\.cs", dll.read_bytes()):
            print(f"  FAIL {dll.name} references {bad.decode()}")
            ok = False
    if ok:
        print("  PASS no res://../ escapes")
    return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="Fork package version (default: detect from .feed)")
    args = parser.parse_args()

    version = args.version or detect_version()
    print(f"Testing fork packages {version}\n")

    prepare(version)
    build(version)

    print("\nScript paths:")
    paths_ok = check_paths()
    print("\nPath sanity:")
    sanity_ok = check_no_broken_paths()

    if not (paths_ok and sanity_ok):
        sys.exit("\nFAIL: multi-assembly integration test failed.")
    print("\nPASS: every type carries the script path its location calls for.")


if __name__ == "__main__":
    main()
