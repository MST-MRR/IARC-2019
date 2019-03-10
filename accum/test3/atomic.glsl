#version 420
 
layout (binding = 1, offset = 0) uniform atomic_uint atRed;
layout (binding = 1, offset = 4) uniform atomic_uint atGreen;
layout (binding = 1, offset = 8) uniform atomic_uint atBlue;
 
in vec4 color;
 
out vec4 colorOut;
 
void main() {
 
    if ((color.r >= color.g) && (color.r >= color.b))
        atomicCounterIncrement(atRed);
    else if (color.g >= color.b)
        atomicCounterIncrement(atGreen);
    else
        atomicCounterIncrement(atBlue);
 
    colorOut = color;
}