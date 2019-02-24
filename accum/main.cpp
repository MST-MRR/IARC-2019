#define GL_GLEXT_PROTOTYPES
#include <GLFW/glfw3.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glext.h>
#include <stdlib.h>
#include <stdio.h>
#include <tuple>

// GL/glext & GL_GLEXT_PROTOTYPES for vbo

static void error_callback(int error, const char* description)
{
    /* On Error */
    fputs(description, stderr);
}
static void key_callback(GLFWwindow* window, int key, int scancode, 
                            int action, int mods)
{
    /* On Keypress */
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GL_TRUE);
}

int main(void)
{
    // init
    GLFWwindow* window;
    
    glfwSetErrorCallback(error_callback);
    
    if (!glfwInit())
        exit(EXIT_FAILURE);
    
    window = glfwCreateWindow(640, 480, "Major Accumulator", 
                                NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwMakeContextCurrent(window);
    
    glfwSetKeyCallback(window, key_callback);
    
    // Change to vbo
    std::tuple<float, float>//, float> 
        point1 = std::make_tuple(0.6f, -0.4f),
        point2 = std::make_tuple(0.f, 0.6f),
        point3 = std::make_tuple(-0.6f, -0.4f);

    // ** // ** // ** // ** // Create VBO

    // main
    while (!glfwWindowShouldClose(window))
    {
        //glColor3f(1.f, 0.f, 0.f);
        
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        
        glViewport(0, 0, width, height);
        
        glClear(GL_COLOR_BUFFER_BIT);
       
        glBegin(GL_LINES);
        
        // ** // ** // ** // ** // Place verticies

        std::apply(glVertex2f, point1);
        std::apply(glVertex2f, point2);

        std::apply(glVertex2f, point3);
        std::apply(glVertex2f, point2);
        
        glEnd();
        
        glfwSwapBuffers(window);
        
        glfwPollEvents();
    }

    // quit
    glfwDestroyWindow(window);    
    glfwTerminate();
    exit(EXIT_SUCCESS);
}