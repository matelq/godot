using Godot;

namespace UpstreamLibModule;

// Deliberately not a [GlobalClass]: this module exists to pull upstream's
// GodotSharp into the graph, not to contribute a script path.
public static class PathHelper
{
    public static Vector2 Midpoint(Vector2 a, Vector2 b) => (a + b) * 0.5f;
}
