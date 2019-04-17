#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include <opencv2/opencv.hpp>

#include <iostream>
#include <stdexcept>
#include <vector>
#include <fstream>

#include "loader.h"





static void glfwError(int id, const char* description){
  std::cout << description << std::endl;
}

class SickOpenGL{
  public:
		GLFWwindow* window;

		const char* vshader = "vertex.glsl";
		const char* fshader = "fragment.glsl";

		const int int_per_vertex = 3;

		// need to change in fragment too
		int w_width = 1024, w_height = 768; 

		GLuint buff_size = w_width * w_height;
		GLsizeiptr buff_data_size = buff_size * sizeof(GLuint);

		GLuint v_count, v_size;
		GLsizeiptr v_data_size;
  	GLfloat *g_vertex_buffer_data;


	SickOpenGL(){
		/*
		* Basic opengl setup.
		*/
		glEnable( GL_DEBUG_OUTPUT );
		glfwSetErrorCallback(&glfwError);

		glewExperimental = true; // Needed for core profile
		if( !glfwInit() )
		{
			fprintf( stderr, "Failed to initialize GLFW\n" );
			throw std::runtime_error("Failed to initialize GLFW.");
		}
	
		glfwWindowHint(GLFW_SAMPLES, 4); // antialiasing
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // 4.3
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

		window = glfwCreateWindow(w_width, w_height, 
						"Texture Buffer Counting Overlap", NULL, NULL);
		if( window == NULL ){
			fprintf(stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.\n");
			glfwTerminate();
			throw std::runtime_error("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.");
		}
		glfwMakeContextCurrent(window); 
		
		glewExperimental=true;
		if (glewInit() != GLEW_OK){
			fprintf(stderr, "Failed to initialize GLEW\n");
			throw std::runtime_error("Failed to initialize GLEW");
		}

		glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
	}

	void set_verticies(const GLuint vertex_count, GLfloat *values){
		/*
		* Call to set verticies. 
		* 3 tuples, 2 sets makes a line.
		*/
		v_count = vertex_count;
		v_size = v_count * int_per_vertex;
		v_data_size = v_size * sizeof(GLfloat);

		g_vertex_buffer_data = new GLfloat[v_size];
		g_vertex_buffer_data = values;
	}

	void run(){
		/*
		* After verticies set, process
		*/
		// init shaders
		GLuint programID = LoadShaders(vshader, fshader);  

		// init vbuffer
		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  
		glGenBuffers(1, &vertexbuffer);
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  
		glBufferData(GL_ARRAY_BUFFER, v_data_size, g_vertex_buffer_data, 
									GL_STATIC_DRAW);

		// init texture, buffer
		GLuint tex, buf;
		GLuint filler[buff_size] = {0};

		glGenBuffers(1, &buf); 
		glBindBuffer(GL_TEXTURE_BUFFER, buf); 
		glBufferData(GL_TEXTURE_BUFFER, buff_data_size, filler, 
									GL_DYNAMIC_COPY); 

		glGenTextures(1, &tex);  
		glBindTexture(GL_TEXTURE_BUFFER, tex); 
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);

		//
		// do i need this shit and what does it do
		//
		glBindImageTexture(0, tex, 0, GL_FALSE, 0, GL_READ_WRITE, 
											GL_R32UI); 

		do{
			glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
			glClearColor(0.0f, 0.0f, 0.4f, 0.0f) ;

			glEnableVertexAttribArray(0);
			glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

			glVertexAttribPointer(0, int_per_vertex, GL_FLOAT, GL_FALSE, 
														0, (void*)0);

			glUseProgram(programID);
			
			glDrawArrays(GL_LINES, 0, v_count);

			glDisableVertexAttribArray(0);
		
			glfwSwapBuffers(window);
			glfwPollEvents();
		} while(glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
						glfwWindowShouldClose(window) == 0);
	}
	
	void convert_output(){
		/*
		* Convert buffer output to opencv mat
		*/
		// vram -> ram
		GLuint *initial = new GLuint[buff_size];
		glGetBufferSubData(GL_TEXTURE_BUFFER, 0, buff_data_size, initial);

		// should be 5 different numbers


		//glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);
		// data in buffer = R32UI

		// buff_size IS a fuckin GLsizeiptr ie fix inital and the
		// test thing i created


		std::vector<GLuint> unique;

		// buffer -> 2d uint vector
		std::vector<std::vector<GLuint>> intermediary;

		for (int i = 0; i < w_height; i++){
			std::vector<GLuint> cache;

			for (int j = 0; j < w_width; j++){
				cache.push_back(initial[i*w_width + w_height]);

				if(std::find(unique.begin(), unique.end(), initial[i*w_width + w_height]) == unique.end()){
					std::cout << initial[i*w_width + w_height] << i << j << std::endl;
					unique.push_back(initial[i*w_width + w_height]);
				}
			}

			intermediary.push_back(cache);
		}


		// vector -> mat
		cv::Mat finish(w_height, w_width, CV_64FC1);
		for(int i=0; i<finish.rows; ++i){
			for(int j=0; j<finish.cols; ++j){
				finish.at<GLuint>(i, j) = intermediary.at(i).at(j);
			}
		}

	/*
		cv::Mat dst;
		cv::normalize(big_ole_mat, dst, 0, 1, cv::NORM_MINMAX);
    cv::imshow("test", dst);
    cv::waitKey(0);*/
	
	}
};


int main(){
  SickOpenGL demo;
  
  const GLuint v_count = 14;
  GLfloat x[v_count*demo.int_per_vertex] = {
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
  demo.set_verticies(v_count , x);

  demo.run(); 

  demo.convert_output();

  return 0;
}
