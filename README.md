# Godot Engine — multi-assembly C# fork

> **Fork notice.** This repository is a fork of [`godotengine/godot`](https://github.com/godotengine/godot) maintained to ship a small set of C# workflow patches that haven't yet made it through upstream review. Upstream's original README is preserved below, unchanged.

## About this fork

**Purpose.** Upstream's `modules/mono` backend assumes all C# code lives in the main Godot project. This fork removes that assumption, so you can split your project across multiple C# assemblies — referenced projects, class libraries, and NuGet packages — the way a normal .NET solution works. It also improves the external-IDE workflow.

**Changes on top of upstream `4.6.2-stable`:**

- **Multi-assembly C# script support** (new `csharp://` path scheme). Scripts defined in `<ProjectReference>` projects and NuGet packages are discovered, registered, and fully usable in the editor — including `[GlobalClass]`, `[Export]`, transitive dependencies, and hot reload. Based on unmerged upstream PR [godotengine/godot#117452](https://github.com/godotengine/godot/pull/117452). Example project: [matelq/GodotMultiAssemblyReference](https://github.com/matelq/GodotMultiAssemblyReference).
- **Automatic C# build on editor focus.** Opt-in editor setting (`dotnet/editor/automatic_build`) that rebuilds the C# project when Godot regains focus after external IDE edits, eliminating the manual Build button click. Based on unmerged upstream PR [godotengine/godot#103657](https://github.com/godotengine/godot/pull/103657).

**Releases.** Prebuilt Windows x64 editor + export templates (Mono/.NET enabled) are attached to [GitHub Releases](https://github.com/matelq/godot/releases), tagged as `<upstream-version>-conv.<N>` — e.g. `4.6.2-conv.1`. Binaries are **unsigned**; Windows SmartScreen may prompt on first launch.

## Using the fork in a C# project

> **⚠️ Do not use the default `Godot.NET.Sdk/4.6.2` from nuget.org with this editor.** Upstream's 4.6.2 NuGet package ships the unpatched source generator and silently produces broken `res://../Script.cs` paths for assembly-backed `[GlobalClass]` scripts, which the editor will then fail to load at runtime.

The fork publishes its own NuGet packages to nuget.org under the `CrackTower.Godot.*` prefix. Reference them directly in your `.csproj`:

```xml
<Project Sdk="CrackTower.Godot.NET.Sdk/4.6.2-conv.1">
  <!-- ... -->
</Project>
```

This transitively pulls in the fork's runtime assemblies and source generator — everything resolves from nuget.org, no manual setup:

| Package | Replaces |
|---|---|
| [`CrackTower.Godot.NET.Sdk`](https://www.nuget.org/packages/CrackTower.Godot.NET.Sdk) | `Godot.NET.Sdk` |
| [`CrackTower.Godot.Sharp`](https://www.nuget.org/packages/CrackTower.Godot.Sharp) | `GodotSharp` |
| [`CrackTower.Godot.SharpEditor`](https://www.nuget.org/packages/CrackTower.Godot.SharpEditor) | `GodotSharpEditor` |
| [`CrackTower.Godot.SourceGenerators`](https://www.nuget.org/packages/CrackTower.Godot.SourceGenerators) | `Godot.SourceGenerators` |

Assembly names (`GodotSharp.dll`, etc.) are unchanged — the engine loads by assembly name, not NuGet ID, so runtime behaviour is identical to a hypothetical upstream release with the same patches.

A working example is at [matelq/GodotMultiAssemblyReference `fork/4.6.2-conv.1`](https://github.com/matelq/GodotMultiAssemblyReference/tree/fork/4.6.2-conv.1).

**Known caveat:** the editor's New C# Project dialog still templates `<Project Sdk="Godot.NET.Sdk/...">`. After creating a fresh C# project, hand-edit the first line of the generated `.csproj` to `CrackTower.Godot.NET.Sdk/<release-version>`. This will be fixed in a future build.

**Tracking upstream.** The fork rebases onto new upstream `4.6.x-stable` patch releases as they land, and will move to `4.7` after a short verification cycle when upstream ships it. See the commit log on the `fork/4.6` branch for the exact patch stack.

---

# Godot Engine

<p align="center">
  <a href="https://godotengine.org">
    <img src="logo_outlined.svg" width="400" alt="Godot Engine logo">
  </a>
</p>

## 2D and 3D cross-platform game engine

**[Godot Engine](https://godotengine.org) is a feature-packed, cross-platform
game engine to create 2D and 3D games from a unified interface.** It provides a
comprehensive set of [common tools](https://godotengine.org/features), so that
users can focus on making games without having to reinvent the wheel. Games can
be exported with one click to a number of platforms, including the major desktop
platforms (Linux, macOS, Windows), mobile platforms (Android, iOS), as well as
Web-based platforms and [consoles](https://godotengine.org/consoles).

## Free, open source and community-driven

Godot is completely free and open source under the very permissive [MIT license](https://godotengine.org/license).
No strings attached, no royalties, nothing. The users' games are theirs, down
to the last line of engine code. Godot's development is fully independent and
community-driven, empowering users to help shape their engine to match their
expectations. It is supported by the [Godot Foundation](https://godot.foundation/)
not-for-profit.

Before being open sourced in [February 2014](https://github.com/godotengine/godot/commit/0b806ee0fc9097fa7bda7ac0109191c9c5e0a1ac),
Godot had been developed by [Juan Linietsky](https://github.com/reduz) and
[Ariel Manzur](https://github.com/punto-) for several years as an in-house
engine, used to publish several work-for-hire titles.

![Screenshot of a 3D scene in the Godot Engine editor](https://raw.githubusercontent.com/godotengine/godot-design/master/screenshots/editor_tps_demo_1920x1080.jpg)

## Getting the engine

### Binary downloads

Official binaries for the Godot editor and the export templates can be found
[on the Godot website](https://godotengine.org/download).

### Compiling from source

[See the official docs](https://docs.godotengine.org/en/latest/engine_details/development/compiling)
for compilation instructions for every supported platform.

## Community and contributing

Godot is not only an engine but an ever-growing community of users and engine
developers. The main community channels are listed [on the homepage](https://godotengine.org/community).

The best way to get in touch with the core engine developers is to join the
[Godot Contributors Chat](https://chat.godotengine.org).

To get started contributing to the project, see the [contributing guide](CONTRIBUTING.md).
This document also includes guidelines for reporting bugs.

## Documentation and demos

The official documentation is hosted on [Read the Docs](https://docs.godotengine.org).
It is maintained by the Godot community in its own [GitHub repository](https://github.com/godotengine/godot-docs).

The [class reference](https://docs.godotengine.org/en/latest/classes/)
is also accessible from the Godot editor.

We also maintain official demos in their own [GitHub repository](https://github.com/godotengine/godot-demo-projects)
as well as a list of [awesome Godot community resources](https://github.com/godotengine/awesome-godot).

There are also a number of other
[learning resources](https://docs.godotengine.org/en/latest/community/tutorials.html)
provided by the community, such as text and video tutorials, demos, etc.
Consult the [community channels](https://godotengine.org/community)
for more information.

[![Code Triagers Badge](https://www.codetriage.com/godotengine/godot/badges/users.svg)](https://www.codetriage.com/godotengine/godot)
[![Translate on Weblate](https://hosted.weblate.org/widgets/godot-engine/-/godot/svg-badge.svg)](https://hosted.weblate.org/engage/godot-engine/?utm_source=widget)
