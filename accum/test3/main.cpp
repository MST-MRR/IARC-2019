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

#include <iostream>

// pragma debug thing in shaders for debug mode

// shared value in texture is shared between program and shader
static void glfwError(int id, const char* description)
{
  std::cout << description << std::endl;
}


class SickOpenGL{
  private:
 	GLFWwindow* window;
  	const GLfloat g_vertex_buffer_data[30] = {
		-1.0f, -1.0f, 0.0f,
		1.0f, 1.0f, 0.0f,
		-1.0f,  1.0f, 0.0f,
		1.0f, -1.0f, 0.0f,
		-1.0f, 0.5f, 0.0f,
		1.0f,  0.5f, 0.0f,
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f
	};
	GLuint v_count = 12;

  public:
	SickOpenGL(){
		glEnable( GL_DEBUG_OUTPUT );
		glfwSetErrorCallback(&glfwError);

		// Init GLFW
		glewExperimental = true; // Needed for core profile
		if( !glfwInit() )
		{
			fprintf( stderr, "Failed to initialize GLFW\n" );
			throw std::runtime_error("Failed to initialize GLFW.");
		}
	
		glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // We want OpenGL 3.3
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
		GLuint programID = LoadShaders("vertex.glsl", "atomic-counter.glsl" );  // Create and compile our GLSL program from the shaders

		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  // Identifies vertex buffer
		glGenBuffers(1, &vertexbuffer);  // Generate 1 buffer, & store identifier in vertexbuffer
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  // The following commands will talk about our 'vertexbuffer' buffer
		
		// Give vertices to OpenGL.
		glBufferData(GL_ARRAY_BUFFER, sizeof(g_vertex_buffer_data), g_vertex_buffer_data, GL_STATIC_DRAW);

		// TODO #~ - Way to pass in verticies

		// GOAL - rw memory directly, synchronize shader calls
		// 		construct data structure in memory

		// TODO #1 - Create texture that works with vbo.
		// layout (rgba32ui) uniform uimage2D demo_texture;  // image format layout qualifier
		GLuint tex, buf;

		glGenBuffers(1, &buf);  // Generate name for buffer
		glBindBuffer(GL_TEXTURE_BUFFER, buf);  // Bind
		glBufferData(GL_TEXTURE_BUFFER, 4096, NULL, GL_DYNAMIC_COPY);  // Allocate data

		glGenTextures(1, &tex);  // Gerate name for texture
		glBindTexture(GL_TEXTURE_BUFFER, tex);  // Bind to buffer texture target to create
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);  // Attatch buffer object to texture as single channel floating point
	// GL_R32F
		glBindImageTexture(0, tex, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI);  // bind for r/w in image unit

		// TODO #2 - Give texture arbitrary value storage.
		// GL_RGBA32F - bits per texel is what is significant for storage
		//GLuint buffer;
/*		GLuint counters;   /// If i comment out all this nothing hapens

		// Generate buffer name and bind it to generic atomic counter
		glGenBuffers(1, &counters);
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, counters);

		// Allocate space for 2 GLuints in buffer
		glBufferData(GL_ATOMIC_COUNTER_BUFFER, sizeof(GLuint),
					NULL, GL_DYNAMIC_COPY);

		// Map buffer & init
		//counters = (GLuint)glMapBuffer(GL_ATOMIC_COUNTER_BUFFER,
		//								GL_WRITE_ONLY);
										// TODO change the write only?
		//counters[0] = 0;
		//glUnmapBuffer(GL_ATOMIC_COUNTER_BUFFER);

		// bind to 0th GL_ATOMIC_COUNTER_BUFFER
		//glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, buffer);
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, counters);
*/

GLuint ac_buffer = 0;
glGenBuffers(1, &ac_buffer);
glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, ac_buffer);
glBufferData(GL_ATOMIC_COUNTER_BUFFER, sizeof(GLuint), NULL, GL_DYNAMIC_DRAW);
glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, 0);

glBindBufferBase(GL_ATOMIC_COUNTER_BUFFER, 0, ac_buffer);

glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, ac_buffer);
GLuint* ptr = (GLuint*)glMapBufferRange(GL_ATOMIC_COUNTER_BUFFER, 0, sizeof(GLuint),
                                        GL_MAP_WRITE_BIT | 
                                        GL_MAP_INVALIDATE_BUFFER_BIT | 
                                        GL_MAP_UNSYNCHRONIZED_BIT);
ptr[0] = value;
glUnmapBuffer(GL_ATOMIC_COUNTER_BUFFER);
glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, 0); 


		glActiveTexture(GL_TEXTURE_BUFFER);

		do{
			// Clear screen
			glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
			glClearColor(0.0f, 0.0f, 0.4f, 0.0f) ;

			// Set buffer
			// 1st attribute buffer : vertices
			glEnableVertexAttribArray(0);
			glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

			glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

			glUseProgram(programID);  // Use shader
			
			// Draw
			// TODO #3 - Draw w/ arbitrary values in texture.
			// can modify variables in texture through fragment shader!

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
