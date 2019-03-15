#version 430
 
layout (binding = 1, offset = 0) uniform atomic_uint at;
 
uniform sampler2D texUnit;
 
in VertexData {
    vec4 color;
    vec4 texCoord;
    float texCount;
} FragmentIn;
 
out vec4 colorOut;
 
void main() {
 
    uint a = atomicCounterIncrement(at);
    //uint b = atomicCounterDecrement(at);
 
    if (a == a)
        colorOut = texture(texUnit, FragmentIn.texCoord.xy);
    else
        colorOut = vec4(1.0, 0.0, 0.0, 1.0);
}