using Godot;

namespace TransitiveModule;

[GlobalClass]
public partial class QuestTracker : Node
{
    [Export] public int ActiveQuests { get; set; }
}
