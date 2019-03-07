#include <stdio.h>
#include <stdlib.h>
// Include GLEW. 
// Always include it before gl.h and glfw3.h
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include "loader.h"
#include <stdexcept>


// pragma debug thing in shaders for debug mode

// make texture and accumulate with again
// shared value in texture is shared between program and shader


class SickOpenGL{
// make into a class and make sure state set before tryna do stuff
  private:
 	GLFWwindow* window;
  	const GLfloat g_vertex_buffer_data[24] = {
		-1.0f, -1.0f, 0.0f,
		1.0f, 1.0f, 0.0f,
		-1.0f,  1.0f, 0.0f,
		1.0f, -1.0f, 0.0f,
		-1.0f, 0.5f, 0.0f,
		1.0f,  0.5f, 0.0f,
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f
	};
	GLuint v_count = 8;

  public:
	SickOpenGL(){
		// Init GLFW
		glewExperimental = true; // Needed for core profile
		if( !glfwInit() )
		{
			fprintf( stderr, "Failed to initialize GLFW\n" );
			throw std::runtime_error("Failed to initialize GLFW.");
		}

		glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // We want OpenGL 3.3
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // We don't want the old OpenGL 

		// Open window & add OpenGL context
		
		window = glfwCreateWindow( 1024, 768, "Texture Accumulating Arbitrary Values", NULL, NULL);
		if( window == NULL ){
			fprintf( stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.\n" );
			glfwTerminate();
			throw std::runtime_error("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.");
		}
		glfwMakeContextCurrent(window); // Initialize GLEW
		
		glewExperimental=true; // Needed in core profile
		if (glewInit() != GLEW_OK) {
			fprintf(stderr, "Failed to initialize GLEW\n");
			throw std::runtime_error("Failed to initialize GLEW");
		}

		// Ensure can capture escape key press
		glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
	}

	void run(){
		GLuint programID = LoadShaders("vertex.glsl", "fragment.glsl" );  // Create and compile our GLSL program from the shaders

		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  // Identifies vertex buffer
		glGenBuffers(1, &vertexbuffer);  // Generate 1 buffer, & store identifier in vertexbuffer
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  // The following commands will talk about our 'vertexbuffer' buffer
		
		// Give vertices to OpenGL.
		glBufferData(GL_ARRAY_BUFFER, sizeof(g_vertex_buffer_data), g_vertex_buffer_data, GL_STATIC_DRAW);

		// TODO #~ - Way to pass in verticies

		// TODO #1 - Create texture that works with vbo.
		// layout (rgba32ui) uniform uimage2D demo_texture;  // image format layout qualifier
		GLuint tex, buf;

		glGenBuffers(1, &buf);  // Generate name for buffer
		glBindBuffer(GL_TEXTURE_BUFFER, buf);  // Bind
		glBufferData(GL_TEXTURE_BUFFER, 4096, NULL, GL_DYNAMIC_COPY);  // Allocate data

		glGenTextures(1, &tex);  // Gerate name for texture
		glBindTexture(GL_TEXTURE_BUFFER, tex);  // Bind to buffer texture target to create
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32F, buf);  // Attatch buffer object to texture as single channel floating point

		glBindImageTexture(0, tex, 0, GL_FALSE, 0, GL_READ_WRITE, GL_RGBA32F);  // bind for r/w in image unit


		// TODO #2 - Give texture arbitrary value storage.
		// GL_RGBA32F - bits per texel is what is significant for storage

/* App declaration */
    // Member variables
    float aspect;

    // Program to construct the linked list (renders the transparent objects)
    GLuint  list_build_program;

    // Color palette buffer texture
    GLuint  image_palette_buffer;
    GLuint  image_palette_texture;

    // Output image and PBO for clearing it
    GLuint  overdraw_count_buffer;
    GLuint  overdraw_count_clear_buffer;

    // Program to render the scene
    GLuint render_scene_prog;
    struct
    {
        GLint aspect;
        GLint time;
        GLint model_matrix;
        GLint view_matrix;
        GLint projection_matrix;
    } render_scene_uniforms;

    // Program to resolve 
    GLuint resolve_program;

    // Full Screen Quad
    GLuint  quad_vbo;
    GLuint  quad_vao;

    GLint current_width;
    GLint current_height;

VBObject object; // a managed vbo that reads from file


/**/
/* Init */

  render_scene_prog = -1;

    base::Initialize(title);

    const GLubyte * vendor = glGetString(GL_VENDOR);
    const GLubyte * renderer = glGetString(GL_RENDERER);
    const GLubyte * version = glGetString(GL_VERSION);

    // Assemble a message
    std::string message = std::string("Created debug context with ") +
                          std::string((const char*)vendor) + std::string(" ") +
                          std::string((const char*)renderer) +
                          std::string(". The OpenGL version is ") +
                          std::string((const char*)version) + std::string(".");

    // Send the message to the debug output log
    glDebugMessageInsert(GL_DEBUG_SOURCE_APPLICATION,
                         GL_DEBUG_TYPE_MARKER,
                         0x4752415A,
                         GL_DEBUG_SEVERITY_NOTIFICATION,
                         0,
                         message.c_str());

    glPushDebugGroup(GL_DEBUG_SOURCE_APPLICATION, 0x4752415A, -1, "Initialization");

    InitPrograms();

    // glPopDebugGroup();

    // Create palette texture
    glGenBuffers(1, &image_palette_buffer);
    glBindBuffer(GL_TEXTURE_BUFFER, image_palette_buffer);
    glBufferData(GL_TEXTURE_BUFFER, 256 * 4 * sizeof(float), NULL, GL_STATIC_DRAW);
    glGenTextures(1, &image_palette_texture);
    glBindTexture(GL_TEXTURE_BUFFER, image_palette_texture);
    glTexBuffer(GL_TEXTURE_BUFFER, GL_RGBA32F, image_palette_buffer);

    vmath::vec4 * data = (vmath::vec4 *)glMapBuffer(GL_TEXTURE_BUFFER, GL_WRITE_ONLY);
    for (int i = 0; i < 256; i++)
    {
        data[i] = vmath::vec4((float)i);
    }
    glUnmapBuffer(GL_TEXTURE_BUFFER);

    // Create overdraw counter texture
    glGenTextures(1, &overdraw_count_buffer);
    glBindTexture(GL_TEXTURE_2D, overdraw_count_buffer);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_R32UI, MAX_FRAMEBUFFER_WIDTH, MAX_FRAMEBUFFER_HEIGHT, 0, GL_RED_INTEGER, GL_UNSIGNED_INT, NULL);
    glBindTexture(GL_TEXTURE_2D, 0);

    // Create buffer for clearing the head pointer texture
    glGenBuffers(1, &overdraw_count_clear_buffer);
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, overdraw_count_clear_buffer);
    glBufferData(GL_PIXEL_UNPACK_BUFFER, MAX_FRAMEBUFFER_WIDTH * MAX_FRAMEBUFFER_HEIGHT * sizeof(GLuint), NULL, GL_STATIC_DRAW);

    data = (vmath::vec4 *)glMapBuffer(GL_PIXEL_UNPACK_BUFFER, GL_WRITE_ONLY);
    memset(data, 0x00, MAX_FRAMEBUFFER_WIDTH * MAX_FRAMEBUFFER_HEIGHT * sizeof(GLuint));
    glUnmapBuffer(GL_PIXEL_UNPACK_BUFFER);

    // Create VAO containing quad for the final blit
    glGenVertexArrays(1, &quad_vao);
    glBindVertexArray(quad_vao);

    static const GLfloat quad_verts[] =
    {
        -1.0f, -1.0f,
         1.0f, -1.0f,
        -1.0f,  1.0f,
         1.0f,  1.0f,
    };

    glGenBuffers(1, &quad_vbo);
    glBindBuffer(GL_ARRAY_BUFFER, quad_vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(quad_verts), quad_verts, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(0);

    glClearDepth(1.0f);

object.LoadFromVBM("media/unit_pipe.vbm", 0, 1, 2);

/**/
/* Init Programs  */
// Create the program for rendering the scene from the viewer's position
    ShaderInfo scene_shaders[] =
    {
        { GL_VERTEX_SHADER, "media/shaders/overdrawcount/overdraw_count.vs.glsl" },
        { GL_FRAGMENT_SHADER, "media/shaders/overdrawcount/overdraw_count.fs.glsl" },
        { GL_NONE }
    };

    if (render_scene_prog != -1)
        glDeleteProgram(render_scene_prog);

    render_scene_prog = LoadShaders(scene_shaders);

    render_scene_uniforms.model_matrix = glGetUniformLocation(render_scene_prog, "model_matrix");
    render_scene_uniforms.view_matrix = glGetUniformLocation(render_scene_prog, "view_matrix");
    render_scene_uniforms.projection_matrix = glGetUniformLocation(render_scene_prog, "projection_matrix");
    render_scene_uniforms.aspect = glGetUniformLocation(render_scene_prog, "aspect");
    render_scene_uniforms.time = glGetUniformLocation(render_scene_prog, "time");

    ShaderInfo resolve_shaders[] =
    {
        { GL_VERTEX_SHADER, "media/shaders/overdrawcount/blit.vs.glsl" },
        { GL_FRAGMENT_SHADER, "media/shaders/overdrawcount/blit.fs.glsl" },
        { GL_NONE }
    };

resolve_program = LoadShaders(resolve_shaders);

/**/

		do{
			// Clear screen
			glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
			glClearColor(0.0f, 0.0f, 0.4f, 0.0f) ;

	/* OpenGL Redbook 9th overdraw */
	float t;

    glDisable(GL_DEPTH_TEST);
    glDisable(GL_CULL_FACE);

    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    // Clear output image
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, overdraw_count_clear_buffer);
    glBindTexture(GL_TEXTURE_2D, overdraw_count_buffer);
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, current_width, current_height, GL_RED_INTEGER, GL_UNSIGNED_INT, NULL);
    glBindTexture(GL_TEXTURE_2D, 0);

    // Bind output image for read-write
    glBindImageTexture(0, overdraw_count_buffer, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI);

    // Render
    glUseProgram(render_scene_prog);

    vmath::mat4 model_matrix = vmath::translate(0.0f, 0.0f, -20.0f) *
                               vmath::rotate(t * 360.0f, 0.0f, 0.0f, 1.0f) *
                               vmath::rotate(t * 435.0f, 0.0f, 1.0f, 0.0f) *
                               vmath::rotate(t * 275.0f, 1.0f, 0.0f, 0.0f);
    vmath::mat4 view_matrix = vmath::mat4::identity();
    vmath::mat4 projection_matrix = vmath::frustum(-1.0f, 1.0f, aspect, -aspect, 1.0f, 40.f);

    glUniformMatrix4fv(render_scene_uniforms.model_matrix, 1, GL_FALSE, model_matrix);
    glUniformMatrix4fv(render_scene_uniforms.view_matrix, 1, GL_FALSE, view_matrix);
    glUniformMatrix4fv(render_scene_uniforms.projection_matrix, 1, GL_FALSE, projection_matrix);

    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE);

    object.Render(0, 8 * 8 * 8);

    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE);

    glBindVertexArray(quad_vao);
    glUseProgram(resolve_program);
glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);



	/**/
			// Set buffer
			// 1st attribute buffer : vertices
			glEnableVertexAttribArray(0);
			glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

			glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

			glUseProgram(programID);  // Use shader
			
			// Draw
			// TODO #3 - Draw w/ arbitrary values in texture.
			glLineWidth(2);
			glDrawArrays(GL_LINES, 0, v_count); // Starting from vertex 0; 3 vertices total -> 1 triangle
			glDisableVertexAttribArray(0);

			// Swap buffers
			glfwSwapBuffers(window);
			glfwPollEvents();

		} // Check if the ESC key was pressed or the window was closed
		while( glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
			glfwWindowShouldClose(window) == 0 );

		// TODO #4 - Output texture values.
	}
};


int main(){
  SickOpenGL demo;

  demo.run(); 

  return 0;
}
