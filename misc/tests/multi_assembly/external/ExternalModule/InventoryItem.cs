using Godot;

namespace ExternalModule;

// A Resource rather than a Node: this is the case pcloves reported on #117452,
// where assembly-backed resources were missing from the Create New Resource
// dialog until an MSBuild rebuild re-registered them.
[GlobalClass]
public partial class InventoryItem : Resource
{
    [Export] public string ItemName { get; set; } = "";
}
