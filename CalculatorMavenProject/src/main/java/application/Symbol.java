package application;

/**
 * Enumerated type for several basic mathematical symbols.
 * 
 * @author ZLAC211
 */
public enum Symbol {
  LEFT_BRACKET("("), RIGHT_BRACKET(")"), TIMES("*"), PLUS("+"), DIVIDE("/"), MINUS("-"), INVALID(
      "INVALID SYMBOL");

  private String printString;

  Symbol(String string) {
    this.printString = string;
  }

  @Override
  public String toString() {
    return printString;
  }

}
