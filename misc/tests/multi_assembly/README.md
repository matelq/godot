# Multi-assembly integration test

Checks that the fork's packaged SDK gives assembly-backed C# scripts usable
paths. Run by CI on every build; `verify.py` is also runnable by hand.

## What it covers

A Godot project whose `[GlobalClass]` types come from three places:

| Type | Lives in | Expected path |
|---|---|---|
| `InventorySystem` (Node) | NuGet package referenced by the project | `csharp://` |
| `InventoryItem` (Resource) | same package | `csharp://` |
| `QuestTracker` (Node) | package referenced *by that package* | `csharp://` |
| `HealthComponent` (Node) | project under the Godot project dir | `res://` |

plus `UpstreamLibModule`, a stand-in third-party library that drags upstream's
`GodotSharp` into the graph (see below).

The Resource case is the one [@pcloves reported on #117452](https://github.com/godotengine/godot/pull/117452);
the transitive case is what breaks when only direct references are scanned.

The failure this exists to catch is upstream's generator emitting
`res://../X.cs` for assembly-backed scripts — a path that escapes `res://`, so
the editor cannot open it and logs `Cannot open file res://../X.cs` on load.
The test therefore also asserts that no built assembly contains such a path.

`UpstreamLibModule` covers a second failure. It stands in for a real
third-party Godot library: built against upstream's `GodotSharp`, knowing
nothing about the fork. Upstream's `GodotSharp.dll` and the fork's have the
same assembly identity under different package ids, so without the SDK
excluding upstream's the main project compiles against the wrong one and fails
with `CS0117` on `LookupScriptsInReferencedAssemblies`. To see that failure,
build the fixture with `-p:DisableImplicitUpstreamGodotSharpExclusion=true`.

This complements `Godot.SourceGenerators.Tests`, which drives the generator
directly. Here the generator arrives the way users get it — through the packed
`CrackTower.Godot.*` NuGet packages — so NuGet packing, the `Sdk.props`/
`Sdk.targets` wiring and transitive package resolution all have to be right.

## Running it

Put the fork packages under test in `.feed/`, then:

```
python verify.py
```

The version is read off the `CrackTower.Godot.Sharp` package in `.feed`; pass
`--version` to override. To test a published release instead of a local build,
download the packages from nuget.org into `.feed/` first.

## What it does not cover

Whether the *editor* registers these classes — the Add Node dialog, the Create
Resource dialog, and the `ScriptServer` probe described in the example
project's `TESTING.md`.

Those still need a manual pass. Driving the editor headless does not work:
`--headless -e` registers only the `res://` classes and silently omits every
assembly-backed one. That reproduces against the known-good example project
too, so it is a property of headless mode rather than of any particular
project — worth investigating on its own, since it also affects anyone trying
to export a multi-assembly project from CI.
