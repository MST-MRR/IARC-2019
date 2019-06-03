#include <iostream>

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include <GL/gl.h>


void GLAPIENTRY MessageCallback(GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam ){fprintf( stderr, "GL CALLBACK: %s type = 0x%x, severity = 0x%x, message = %s\n", ( type == GL_DEBUG_TYPE_ERROR ? "** GL ERROR **" : "" ), type, severity, message );}
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
	// TODO
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

		glEnable              (GL_DEBUG_OUTPUT);
		glDebugMessageCallback(MessageCallback, 0);
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

		g_vertex_buffer_data = new GLfloat[VSIZE];
		g_vertex_buffer_data = vertex_values;
	}
};

int main(){
	TSSpace space;

	return 0;
}

extern "C" {
	TSSpace* init_ts(){ return new TSSpace(); }
	TSSpace* parameterized_init_ts(const GLuint v_count, GLfloat *verticies){return new TSSpace(v_count, verticies);}
}