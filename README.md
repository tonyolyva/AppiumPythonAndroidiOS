# AppiumPythonAndroidiOS - A Feature-Rich Web Calculator
AppiumPythonAndroidiOS is a test framework for Android Calculator and iOS CalculMath. 

## Calc Features
* **Basic Arithmetic Operations:** Addition, subtraction, multiplication, and division.
* **Unary Operations:**
    * Square (x²)
    * Square root (√)
    * Cube (x³)
    * Cube root (∛)
    * Reciprocal (1/x)
    * Factorial (x!)
    * Power of two (2ˣ)
    * Power of ten (10ˣ)
* **Exponentiation:** xʸ (power function)
* **Decimal Input:** Supports decimal numbers and negative inputs.
* **Clear Functionality:** Clears the display and resets the calculator.
* **Error Handling:** Handles division by zero, invalid input, and other potential errors.
* **Clean Architecture:** Uses a ViewModel to separate UI logic from business logic.
* **Test-Driven Development:** Includes unit tests and UI tests to ensure code quality.
* **SwiftUI:** Built with SwiftUI for a modern and declarative UI.

## Installation
1.  **Clone the repository:**

    ```bash
    git clone https://github.com/tonyolyva/AppiumPythonAndroidiOS.git
    ```

## Usage
* **Basic Operations:** Use the number buttons to input values, and the operation buttons (+, -, \*, /) to perform calculations. Press "=" to get the result.
* **Unary Operations:** Press the corresponding unary operation button (x², √, x³, ∛, 1/x, x!, 2ˣ, 10ˣ) to perform the operation on the current value.
* **Exponentiation:** Press the "xʸ" button, input the exponent, and press "=".
* **Decimal Input:** Press the "." button to input decimal numbers.
* **Negative Input:** Press the "-" button before inputting a number to make it negative.
* **Clear:** Press the "C" button to clear the display and reset the calculator.

## Architecture
* **`AppiumPythonAndroidiOSTests`:** Unit tests to verify the calculator's functionality.
* **`AppiumPythonAndroidiOSUITests`:** UI tests to verify the user interface's behavior.

## Testing
The project includes unit tests and UI tests to ensure code quality and functionality.

* **Unit Tests:** Located in the `AppiumPythonAndroidiOSTests` group. These tests verify the core calculator logic and calculations.
* **UI Tests:** Located in the `AppiumPythonAndroidiOSUITests` group. These tests verify the user interface's behavior and interactions.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author
* tonyolyva
* GitHub Profile: https://github.com/tonyolyva/

## Contact
* olyvatony@gmail.com
* https://www.linkedin.com/in/anatoliy-olyva-a9b3b718b/

## Acknowledgments
* Used BigInt librariy for Factorial functionality