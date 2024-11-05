#define N 500
// Define the base color for shadowed areas
#define SHADOW_COLOR vec4(0.0, 1.0, 1.0, 1.0)
// x, y position of the light
uniform vec2 lightPosition;
// Size of light in pixels
uniform float lightSize;

float terrain(vec2 samplePoint)
{
    // Returns a score between 0.0 and 1.0 based on the alpha value of the texture(framebuffer at iChannel0)
    // Used to identify if the sample point is free space(terrain)
    // Terrains are the shadowed areas

    // Read the alpha value of the same pixel at channel 0
    float samplePointAlpha = texture(iChannel0, samplePoint).a;

    // Step function returns 1.0 if the first argument is less than the second, otherwise 0.0
    float sampleStepped = step(0.1, samplePointAlpha);

    // Inverse the step score (since returnValue = 1 means terrain)
    float returnValue = 1.0 - sampleStepped;

    // The closer the first number(0.98) is to 1.0, the softer the shadows.
    // The first value being 0.0 will create sharp edges.
    returnValue = mix(0.98, 1.0, returnValue);

    return returnValue;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // fragCoord is the pixel coordinate of the current pixel
    // fragColor is the color of the current pixel (this is what shader calculates)

    // Distance in pixels to the light
    // lightPosition is read from python (x, y) and passed to the shader
    // default is the use the player's coordinate
    float distanceToLight = length(lightPosition - fragCoord);

    // Normalize the fragment coordinate from (0.0, 0.0) to (1.0, 1.0)
    vec2 normalizedFragCoord = fragCoord/iResolution.xy;
    vec2 normalizedLightCoord = lightPosition.xy/iResolution.xy;

    // We are going to calculate the pixel value by mixing between the shadow color and the color of the texture
    // (texture: original pixel color value in channel 1)
    // If the pixel is in shadow, we'll use the shadow color
    // If the pixel is in light, we'll use the color of the texture (original pixel color)
    // Start our mixing variable at 1.0
    float lightAmount = 1.0;

    // We divide the distance between the light source (player's position) and the current pixel into N steps
    // We'll check each step to see if there is something in the way
    // If there is, we'll reduce the light amount
    for(float i = 0.0; i < N; i++)
    {
        // A ratio in [0.0, 1.0] between where our current pixel is, and where the light is
        float t = i / N;
        // Grab a coordinate between where the current pixel is and the light source
        vec2 samplePoint = mix(normalizedFragCoord, normalizedLightCoord, t);

        // Is there something there? If so, we'll assume we are in shadow
	    float shadowAmount = terrain(samplePoint);
        // Multiply the light amount.
        lightAmount *= shadowAmount;
    }

    // Find out how much light we have based on the distance to our light
    // Note that smoothstep reduces the light almost linearly, it should be by the square of the distance
    // Improve later
    lightAmount *= 1.0 - smoothstep(0.0, lightSize, distanceToLight);

    // We'll alternate our display between shadow and whatever is in channel 1
    // Our fragment color will be somewhere between SHADOW_COLOR and channel 1
    // lightAmount is a value between [0.0, 1.0]
    // if lightAmount is 0.0, the pixel has SHADOW_COLOR
    // if lightAmount is 1.0, the pixel has the original color
    fragColor = mix(SHADOW_COLOR, texture(iChannel1, normalizedFragCoord), lightAmount);
}