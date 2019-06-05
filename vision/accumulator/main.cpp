// C++11+

#include <iostream>
#include <cstdint>

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include <opencv2/opencv.hpp>

#include "shader_loader.h"

//DEBUG
//void GLAPIENTRY MessageCallback(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam ){fprintf( stderr, "GL CALLBACK: %s type = 0x%x, severity = 0x%x, message = %s\n", ( type == GL_DEBUG_TYPE_ERROR ? "** GL ERROR **" : "" ), type, severity, message );}

static void glfwError(int id, const char* description){std::cout << description << std::endl;}
const int INT_PER_VERTEX = 3;

class TSSpace{
  public:
		GLFWwindow* window;

		const char* vshader = "shaders/vertex.glsl";
		const char* fshader = "shaders/fragment_accumulator.glsl";

		// Width in fragment_accumulator as magic number
		int WIDTH = 1024, HEIGHT = 768; 

		GLuint BUFF_SIZE = WIDTH * HEIGHT;
		GLsizeiptr BUFF_DATA_SIZE = BUFF_SIZE * sizeof(GLuint);

		GLuint tex, buf;

		GLuint image_unit = 0;

		GLuint VCOUNT, VSIZE;
		GLsizeiptr VERTEX_DATA_SIZE;
  		GLfloat *g_vertex_buffer_data = nullptr;

  	TSSpace(){
		/* 
		@fn TSSpace
		@breif Setup opengl.
		*/
		setup_opengl();
	}

	TSSpace(const GLuint vertex_count, GLfloat *vertex_values){
		/* 
		@fn TSSpace
		@breif Setup opengl and set verticies.

		@param vertex_count uint Number of 3D verticies in 
				vertex_values.
		@param vertex_values Glfloat* XYZ locations of verticies, 
				every 2 values is a line.
		*/
		setup_opengl();

		set_verticies(vertex_count , vertex_values);
	}

	void setup_opengl(){
		/*
		@fn setup_opengl
		@breif Do all of the opengl window setup.
		*/
		glEnable( GL_DEBUG_OUTPUT );
		glfwSetErrorCallback(&glfwError);

		//DEBUG
		//glDebugMessageCallback(MessageCallback, 0);

		glewExperimental = true; // Needed for core profile
		if(!glfwInit()){
			fprintf( stderr, "Failed to initialize GLFW\n" );
			throw std::runtime_error("Failed to initialize GLFW.");
		}
	
		glfwWindowHint(GLFW_SAMPLES, 1); // antialiasing
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // 4.3
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

		window = glfwCreateWindow(WIDTH, HEIGHT, "TS Space", NULL, NULL);
		if(window == NULL){
			glfwTerminate();

			fprintf(stderr, "Failed to open GLFW window.\n");
			throw std::runtime_error("Failed to open GLFW window.");
		}
		glfwMakeContextCurrent(window); 
		
		glewExperimental=true;
		if (glewInit() != GLEW_OK){
			fprintf(stderr, "Failed to initialize GLEW\n");
			throw std::runtime_error("Failed to initialize GLEW");
		}
	}

	void set_verticies(const GLuint vertex_count, GLfloat *vertex_values){
		/* 
		@fn set_verticies
		@breif Sets space verticies to create lines.

		@param vertex_count uint Number of 3D verticies in 
				vertex_values.
		@param vertex_values Glfloat* XYZ locations of verticies, 
				every 2 values is a line.
		*/
		VCOUNT = vertex_count;
		VSIZE = VCOUNT * INT_PER_VERTEX;
		VERTEX_DATA_SIZE = VSIZE * sizeof(GLfloat);

		g_vertex_buffer_data = vertex_values;
	}

	void accumulate(){
		/* 
		@fn accumulate
		@breif Counts number of lines drawn on each pixel.

		@pre Opengl is initialized, verticies are set and shaders exist.
		*/

		// setup
		GLuint filler[BUFF_SIZE] = {0};

		glGenBuffers(1, &buf);
		glBindBuffer(GL_TEXTURE_BUFFER, buf);
		glBufferData(GL_TEXTURE_BUFFER, BUFF_DATA_SIZE, filler, 
			GL_DYNAMIC_COPY);

		glGenTextures(1, &tex);

		glBindTexture(GL_TEXTURE_BUFFER, tex); 
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);

		glBindImageTexture(image_unit, tex, 0, GL_FALSE, 0, 
			GL_READ_WRITE, GL_R32UI); 

		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  
		glGenBuffers(1, &vertexbuffer);
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  
		glBufferData(GL_ARRAY_BUFFER, VERTEX_DATA_SIZE, 
			g_vertex_buffer_data, GL_STATIC_DRAW);

		GLuint programID = LoadShaders(vshader, fshader); 

		//glOrtho(0, WIDTH, HEIGHT, 0, 0, 1);

		// process
		//do {
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glClearColor(0.0f, 0.0f, 0.0f, 0.0f) ;

		glEnableVertexAttribArray(0);
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

		glVertexAttribPointer(0, INT_PER_VERTEX, GL_FLOAT, GL_FALSE, 
			0, (void*)0);

 		glUseProgram(programID);
		
		glDrawArrays(GL_LINES, 0, VCOUNT);

		glDisableVertexAttribArray(0);
	
		glfwSwapBuffers(window);
		
		// DEBUG
		//glfwPollEvents();
		//}while( glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS && glfwWindowShouldClose(window) == 0 );
	}

	void convert_output(uint32_t * output){
		/* 
		@fn convert_output
		@breif Convert processed data into opencv mat.

		@pre Buffer id buf contains processed values. Size allocated at output = BUFF_SIZE.

		@param output uint* Location of gpu buffer to end go.
		*/
		glGetNamedBufferSubData(buf, 0, BUFF_DATA_SIZE, output);
		glfwDestroyWindow(window);  // cannot destroy window before read
	}
};

int main(){
  // sanity check
  const GLuint VCOUNT = 10;
  GLfloat verticies[VCOUNT*INT_PER_VERTEX] = {
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
		};

  TSSpace tsspace(VCOUNT , verticies);

  tsspace.accumulate();

  uint32_t * data = new uint32_t[tsspace.BUFF_SIZE];

  tsspace.convert_output(data);

  delete[] data;
  std::cout << "check" << std::endl;

  return 0;
}


typedef void*(*allocator_t)(int, int*);
extern "C" {
	TSSpace* init_ts(){ return new TSSpace(); }
	TSSpace* parameterized_init_ts(const GLuint v_count, GLfloat *verticies){return new TSSpace(v_count, verticies);}
	void accumulate(TSSpace* space){space->accumulate();}

	void convert_output(TSSpace* space, allocator_t allocator){
		int dims[] = {space->HEIGHT, space->WIDTH};
		uint32_t * data = (uint32_t*) allocator(2, dims);

		space->convert_output(data);

	}

}