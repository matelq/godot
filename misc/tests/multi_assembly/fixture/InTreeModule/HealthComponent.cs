using Godot;

namespace InTreeModule;

[GlobalClass]
public partial class HealthComponent : Node
{
    [Export] public int MaxHealth { get; set; } = 100;
}
