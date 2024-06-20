#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

/* button input GPIOs (gpiochip0) */
#define BUTTON_RIGHT	19
#define BUTTON_LEFT	25
#define BUTTON_UP	26
#define BUTTON_DOWN	24

/* limit input GPIOs (gpiochip2) */
#define LIMIT_X_LEFT	0
#define LIMIT_X_RIGHT	1

/* motor output GPIOs (gpiochip2) */
#define MOTOR_X_LEFT	7
#define MOTOR_X_RIGHT	8

#define IN 1
#define OUT 0

struct gpiod_line *get_gpiod_line(struct gpiod_chip *chip, int gpio, 
		char *name, int input){
	struct gpiod_line *line;
	line = gpiod_chip_get_line(chip, gpio);
	if (input){
		gpiod_line_request_input(line, name);
	} else {
		gpiod_line_request_output(line, name, 1);
	}
	return line;
}

int main(int argc, char **argv)
{
	struct gpiod_chip *chip_pi;
	struct gpiod_chip *chip_goldi;
	struct gpiod_line *b_right_line, *b_left_line, *b_up_line;
	struct gpiod_line *lx_right_line, *lx_left_line;
	struct gpiod_line *mx_right_line, *mx_left_line;

	chip_pi = gpiod_chip_open_by_name("gpiochip0");
	chip_goldi = gpiod_chip_open_by_name("gpiochip2");

	b_right_line= 
		get_gpiod_line(chip_pi, BUTTON_RIGHT, "button_right", IN);
	b_left_line = 
		get_gpiod_line(chip_pi, BUTTON_LEFT, "button_left", IN);
	b_up_line = 
		get_gpiod_line(chip_pi, BUTTON_UP, "button_up", IN);

	lx_right_line = 
		get_gpiod_line(chip_goldi, LIMIT_X_RIGHT, "limit_x_right", IN);
	lx_left_line = 
		get_gpiod_line(chip_goldi, LIMIT_X_LEFT, "limit_x_left", IN);

	mx_right_line = 
		get_gpiod_line(chip_goldi, MOTOR_X_RIGHT, "motor_x_right", OUT);
	mx_left_line =
		get_gpiod_line(chip_goldi, MOTOR_X_LEFT, "motor_x_left", OUT);

	while (gpiod_line_get_value(b_up_line)) {
		if (!gpiod_line_get_value(b_right_line) && 
				!(gpiod_line_get_value(lx_right_line))){
			gpiod_line_set_value(mx_right_line, 1);
		} else {
			gpiod_line_set_value(mx_right_line, 0);
		}
		if (!gpiod_line_get_value(b_left_line) && 
				!(gpiod_line_get_value(lx_left_line))){
			gpiod_line_set_value(mx_left_line, 1);
		} else {
			gpiod_line_set_value(mx_left_line, 0);
		}
		usleep(10000);
	}

release_line:
	gpiod_line_release(b_right_line);
	gpiod_line_release(b_left_line);
	gpiod_line_release(b_up_line);
	gpiod_line_release(lx_right_line);
	gpiod_line_release(lx_left_line);
	gpiod_line_release(mx_right_line);
	gpiod_line_release(mx_left_line);
	gpiod_chip_close(chip_goldi);
	gpiod_chip_close(chip_pi);
	return 0;
}
