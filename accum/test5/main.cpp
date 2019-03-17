#include <stdio.h>
#include <stdlib.h>
// Include glew before gl.h and glfw3.h
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include <iostream>
#include <stdexcept>
#include "loader.h"

// pragma debug thing in shaders for debug mode

// shared value in texture is shared between program and shader
static void glfwError(int id, const char* description)
{
  std::cout << description << std::endl;
}


/// figure out how textures work



class SickOpenGL{
  private:
 	GLFWwindow* window;
	static const GLuint v_count = 14;
  	const GLfloat g_vertex_buffer_data[v_count*3] = {
		-1.0f, -1.0f, 0.0f,
		1.0f, 1.0f, 0.0f,
		-1.0f,  1.0f, 0.0f,
		1.0f, -1.0f, 0.0f,
		-1.0f, 0.5f, 0.0f,
		1.0f,  0.5f, 0.0f,

		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,

		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,
		
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,
		
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f
	
	};

	const char* vshader = "vertex.glsl";
	const char* fshader = "fragment.glsl";

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
		GLuint programID = LoadShaders(vshader, fshader);  // Create and compile our GLSL program from the shaders

		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  // Identifies vertex buffer
		glGenBuffers(1, &vertexbuffer);  // Generate 1 buffer, & store identifier in vertexbuffer
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  // The following commands will talk about our 'vertexbuffer' buffer
		
		// Give vertices to OpenGL.
		glBufferData(GL_ARRAY_BUFFER, sizeof(g_vertex_buffer_data), g_vertex_buffer_data, GL_STATIC_DRAW);

	   // Texture creation with buffer binded to image unit? p572
		GLuint tex, buf;

		glGenBuffers(1, &buf);  // Generate name for buffer
		glBindBuffer(GL_TEXTURE_BUFFER, buf);  // Bind
		glBufferData(GL_TEXTURE_BUFFER, 4096, NULL, GL_DYNAMIC_COPY);  // Allocate data

		glGenTextures(1, &tex);  // Gerate name for texture
		glBindTexture(GL_TEXTURE_BUFFER, tex);  // Bind to buffer texture target to create
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);  // Attatch buffer object to texture as single channel floating point

		glBindImageTexture(0, tex, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI);  // bind for r/w in image unit
/*
//http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-14-render-to-texture/
GLuint FramebufferName = 0;
glGenFramebuffers(1, &FramebufferName);
glBindFramebuffer(GL_FRAMEBUFFER, FramebufferName);


// The texture we're going to render to
GLuint renderedTexture;
glGenTextures(1, &renderedTexture);

// "Bind" the newly created texture : all future texture functions will modify this texture
glBindTexture(GL_TEXTURE_2D, renderedTexture);

// Give an empty image to OpenGL ( the last "0" )
glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB, 1024, 768, 0,GL_RGB, GL_UNSIGNED_BYTE, 0);

// Poor filtering. Needed !
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);



// Frame buffer

// Set "renderedTexture" as our colour attachement #0
glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, renderedTexture, 0);

// Set the list of draw buffers.
GLenum DrawBuffers[1] = {GL_COLOR_ATTACHMENT0};
glDrawBuffers(1, DrawBuffers); // "1" is the size of DrawBuffers

if(glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE)
return;

*/





//https://www.khronos.org/opengl/wiki/Shader_Storage_Buffer_Object
int *data = NULL;

GLuint ssbo;
GLsizeiptr size = sizeof(GLuint);

glGenBuffers(1, &ssbo);
glBindBuffer(GL_SHADER_STORAGE_BUFFER, ssbo);
glBufferData(GL_SHADER_STORAGE_BUFFER, size, data, GL_DYNAMIC_DRAW);
glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 6, ssbo);
// uses layout qualifier 6


glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0); // unbind

		do{
			// Counting is done in texture or associated buffer.
			// TODO Why is it not double counting overlaps

			// Clear screen
			glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
			glClearColor(0.0f, 0.0f, 0.4f, 0.0f) ;

			// Set vertex buffer
			// 1st attribute buffer : vertices
			glEnableVertexAttribArray(0);
			glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

			glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

			glUseProgram(programID);  // Use shader
		/*
// Render to our framebuffer
glBindFramebuffer(GL_FRAMEBUFFER, FramebufferName);
glViewport(0,0,1024,768); // Render on the whole framebuffer,
*/


			// Draw
			glDrawArrays(GL_LINES, 0, v_count); // Starting from vertex 0; 3 vertices total -> 1 triangle
			glDisableVertexAttribArray(0);

			// Swap buffers
			glfwSwapBuffers(window);
			glfwPollEvents();

		} // Check if the ESC key was pressed or the window was closed
		while( glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
			glfwWindowShouldClose(window) == 0 );
/*
	   // Output atomic values
		//GLuint *userCounters;
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, atomicsBuffer);
		// again we map the buffer to userCounters, but this time for read-only access
		userCounters = (GLuint*)glMapBufferRange(GL_ATOMIC_COUNTER_BUFFER, 
							0, 
							sizeof(GLuint) * 3,
							GL_MAP_READ_BIT
							);
	
		// copy the values to other variables because...
		GLuint redPixels = userCounters[0],
			   greenPixels = userCounters[1],
			   bluePixels = userCounters[2];
		// ... as soon as we unmap the buffer
		// the pointer userCounters becomes invalid.
		glUnmapBuffer(GL_ATOMIC_COUNTER_BUFFER);

		std::cout << "Counters: " << redPixels 
				<< " " << greenPixels 
				<< " " << bluePixels << std::endl;
		
		if (redPixels > 0 || greenPixels > 0 || bluePixels > 0)
			std::cout << "woooooo u did it\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!\n!!!!!!" << std::endl;
*/
	}
};


// pg 581 on atomic adding to a specific coordinate


// Goal is to make atomic buffer that is the size of the image.
// Then for every x,y that gets a pixel written to, the 
// corresponding buffer can also be incremented.

// Currently there is just 3 counters, added to regardless of
// location.

//// Possible issues
// May be the case that the shader isn't binding to the atomic buffer.

//// Goals
// 1. TODO - COUNTERS WORKING BUT WITH TEXUTRE?
// !!! COUNTERS NOT BEING RESET!!!
// 2. Add to counters based on x,y rather than color.
// 3. Increase size of buffer to image size and increment when
// 	  fragment called at pixel
// 4. Output whole vector
// 5. Allow vertex input.

int main(){
  SickOpenGL demo;

  demo.run(); 

  return 0;
}
