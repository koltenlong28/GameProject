import turtle  
  
def move_obj(ball):  
  
    ball.fillcolor('yellow')  
  
    ball.begin_fill()  
  
    ball.circle(25)  
  
    ball.end_fill()  
  
  
if __name__ == "__main__":  
  
    scr = turtle.Screen()  
  
    scr.setup(650, 650)  
      
    scr.bgcolor('light green')  
  
    scr.tracer(0)  
  
    ball = turtle.Turtle()  
  
    ball.color('red')  
  
    ball.speed(0)  
  
    ball.width(2)  
  
    ball.hideturtle()  
  
    ball.penup()  
  
    ball.goto(0, 350)  
      
    ball.right(90)  
      
    ball.pendown()  
  
    while True:  
  
        ball.clear()  
  
        move_obj(ball)  
  
        scr.update() 
         
        ball.forward(0.6)  
