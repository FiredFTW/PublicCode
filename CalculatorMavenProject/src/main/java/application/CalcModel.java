package application;

/**
 * Evaluates an expression - the evaluation can be Standard (infix) or reverse polish.
 */
public class CalcModel implements Calculator {
  private RevPolishCalc postfixCalc = new RevPolishCalc();
  private StandardCalc infixCalc = new StandardCalc();


  /**
   * Evaluates a mathematical expression written in postfix or infix notation.
   * 
   * @param expression - the expression to be evaluated
   * @param o - the calculation mode, either standard(infix) or reverse polish(postfix)
   * @return the answer to the calculation
   * @throws InvalidExpression if the expression cannot be evaluated (incorrect formatting or
   *         unrecognised tokens)
   */
  public float evaluate(String expression, OpType o) throws InvalidExpression {
    if (o == OpType.STANDARD) {
      return infixCalc.evaluate(expression);
    } else {
      return postfixCalc.evaluate(expression);
    }
  }
  
  
}
