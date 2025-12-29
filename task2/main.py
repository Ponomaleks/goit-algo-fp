from math import sqrt
import turtle

scale = 1 / sqrt(2)


def draw_pythagoras_tree(t, level, size: float = 100) -> None:
    t.left(45)
    t_right = t.clone()
    t_right.right(90)
    t.fd(size)
    t_right.fd(size)

    if level > 0:
        draw_pythagoras_tree(t, level - 1, size * scale)
        draw_pythagoras_tree(t_right, level - 1, size * scale)


def main(level: int = 5, size: float = 200) -> None:
    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.setheading(90)
    t.sety(-turtle.screensize()[1] / 1.5)
    t.pendown()
    t.fd(size)
    draw_pythagoras_tree(t, level, size * scale)
    window.mainloop()


if __name__ == "__main__":
    main(6, 200)
