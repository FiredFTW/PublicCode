package application;

/**
 * Calculator for evaluating and validating postfix expressions.
 * 
 * @author ZLAC211
 */
public class RevPolishCalc {
  NumStack stack;

  /**
   * Evaluates a single postfix expression.
   * 
   * @param expression - the expression to be evaluated
   * @return the answer to the expression
   * @throws InvalidExpression if the input is not a postfix expression with terms and operators
   *         separated by whitespace
   */
  public float evaluate(String expression) throws InvalidExpression {
    stack  = new NumStack(); //make new stack each time so nothing left over from last calculation
    String[] tokens = expression.trim().split("\\s+");
    for (String token : tokens) {
      if (isNumeric(token)) { // if token is a number then push it to stack
        stack.push(Float.parseFloat(token));
      } else {
        try { // otherwise perform current operator on last two numbers and store result
          float operand2 = stack.pop();
          float operand1 = stack.pop();
          float result = performOperation(token, operand1, operand2);
          stack.push(result);
        } catch (EmptyStackException e) {
          throw new InvalidExpression();
        }
      }
    }
    try {
      if (stack.size() != 1) {
        throw new EmptyStackException();
      }
      return stack.pop(); // return final value
    } catch (EmptyStackException e) {
      throw new InvalidExpression();
    }
  }

  /**
   * Determines if a token is a float.
   * 
   * @param token - the token to be tested
   * @return true if the token is a float, else false
   */
  public boolean isNumeric(String token) {
    try {
      Float.parseFloat(token);
      return true;
    } catch (NumberFormatException n) {
      return false;
    }
  }

  /**
   * Performs a simple arithmetic operation on a pair of floats.
   * 
   * @param operator - defines the operation to be executed
   * @param num1 - the first operand
   * @param num2 - the second operand
   * @return the result of performing the operation on the two inputs
   * @throws InvalidExpression if the token passed as an operator is not one of the following: *, /,
   *         +, -
   */
  public static float performOperation(String operator, float num1, float num2)
      throws InvalidExpression {
    switch (operator) {
      case "+":
        return num1 + num2;
      case "-":
        return num1 - num2;
      case "/":
        if (num2 == 0) {
          throw new InvalidExpression();
        }
        return num1 / num2;
      case "*":
        return num1 * num2;
      default:
        throw new InvalidExpression();
    }
  }

}
