package application;

/**
 * Caclulator to compute infix expressions.
 * 
 * @author ZLAC211
 */
public class StandardCalc {
  private RevPolishCalc revCalc = new RevPolishCalc();
  private OpStack opStack;

  /**
   * Evaluates an infix expression.
   * 
   * @param expression - the expression to be evaluated
   * @return the result of the expression
   * @throws InvalidExpression if the input is not an infix expression with terms and operators
   *         separated by whitespace
   */
  public float evaluate(String expression) throws InvalidExpression {
    try {
      //check if expression is already infix, in which case shouldn't work in standard mode
      revCalc.evaluate(expression); 
    } catch (InvalidExpression e) {
      return revCalc.evaluate(convertToPostfix(expression));
    }
    throw new InvalidExpression();

  }

  private String convertToPostfix(String expression) {
    StringBuilder postfix = new StringBuilder();
    String[] tokens = expression.trim().split("\\s+");
    opStack = new OpStack();

    try {
      for (String token : tokens) {
        if (revCalc.isNumeric(token)) {
          postfix.append(token + " ");
        } else if (token.equals("(")) { // beginning of subexpression
          opStack.push(token);
        } else if (token.equals(")")) { // end of subexpression
          while (opStack.size() != 0 && !opStack.top().equals("(")) {
            postfix.append(opStack.pop() + " ");
          }
          if (opStack.size() != 0 && opStack.top().equals("(")) {
            opStack.pop(); // Discard the "("
          } else {
            // Mismatched parentheses
            return "INVALID EXPRESSION";
          }
        } else {
          while (opStack.size() != 0 && precedence(token) <= precedence(opStack.top())) {
            postfix.append(opStack.pop() + " ");
          }
          opStack.push(token);

        }
      }

      while (opStack.size() != 0) {
        postfix.append(opStack.pop() + " ");
      }
    } catch (EmptyStackException e) {
      return "INVALID EXPRESSION";
    }
    return postfix.toString();
  }

  // method to determine the precedence of operators
  private int precedence(String operator) {
    switch (operator) {
      case "+":
      case "-":
        return 1;
      case "*":
      case "/":
        return 2;
      default:
        return -1;
    }


  }



}
