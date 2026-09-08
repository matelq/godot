using Godot;

namespace ExternalModule;

[GlobalClass]
public partial class InventorySystem : Node
{
    [Export] public int Capacity { get; set; } = 10;
}
