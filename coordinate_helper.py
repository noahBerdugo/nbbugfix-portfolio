from pynput import mouse
import time

print("\\nMove your mouse to the desired point in the browser window and press Ctrl+C to quit.")
print("Coordinates will print every second. Use these to fine-tune your click_by_coordinates() call.\\n")

try:
    while True:
        def on_move(x, y):
            print(f"Current mouse position: ({x}, {y})", end='\\r')

        with mouse.Listener(on_move=on_move) as listener:
            time.sleep(1)
except KeyboardInterrupt:
    print("\\nExiting coordinate helper.")
