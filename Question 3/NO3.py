import math
import turtle
 
# Recursive function to draw one edge of the fractal polygon
def draw(length: float, depth: int, inward: bool = True) -> None:
    # Base case: if no more depth, just draw a straight line
    if depth == 0:
        turtle.forward(length)
        return
 
    # Divide the current line into 3 equal parts
    length /= 3.0
 
    # Choose turning angles depending on inward or outward pattern
    if inward:
        t1, t2 = 60, -120   # inward angles
    else:
        t1, t2 = -60, 120   # outward angles
 
    # Recursive calls to draw smaller segments
    draw(length, depth - 1, inward)
    turtle.left(t1)
    draw(length, depth - 1, inward)
    turtle.left(t2)
    draw(length, depth - 1, inward)
    turtle.left(t1)
    draw(length, depth - 1, inward)
 
# Function to set up the polygon and call recursive drawing
def draw_pattern(sides: int, side_length: float, depth: int) -> None:
    # Input validation
    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")
    if side_length <= 0:
        raise ValueError("Side length must be positive.")
    if depth < 0:
        raise ValueError("Recursion depth must be 0 or greater.")
 
    # Set up turtle screen
    screen = turtle.Screen()
    screen.title("Recursive Indented Polygon (Inward)")
    screen.setup(width=1000, height=800)
 
    # Configure turtle
    turtle.hideturtle()
    turtle.speed(0)        # fastest speed
    turtle.pensize(2)      # pen thickness
    screen.tracer(0, 0)    # turn off animation for faster drawing
 
    # Calculate radius of the circumscribed circle for positioning
    r = side_length / (2.0 * math.tan(math.pi / sides))
 
    # Move turtle to starting position
    turtle.penup()
    turtle.setheading(0)    
    turtle.goto(-side_length / 2.0, -r)  # start at bottom of polygon
    turtle.pendown()
 
    # Angle to turn at each vertex
    exterior_turn = 360.0 / sides
 
    # Draw each side of the polygon with recursive indentation
    for _ in range(sides):
        draw(side_length, depth, inward=True)
        turtle.left(exterior_turn)
 
    # Update screen and finish
    screen.update()
    turtle.done()
 
# Main function to collect user input
def main():
    try:
        # Get user inputs
        sides = int(input("Enter the number of sides: "))
        side_length = float(input("Enter the side length (pixels): "))
        depth = int(input("Enter the recursion depth: "))
    except ValueError:
        # Handle invalid input
        print("Please enter valid numeric values (integers for sides/depth, number for length).")
        return
 
    # Call draw function with user input
    draw_pattern(sides, side_length, depth)
 
# Run main only when executed directly
if __name__ == "__main__":
    main()
