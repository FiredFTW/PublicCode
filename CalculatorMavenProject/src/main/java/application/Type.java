package application;

/**
 * Enumerated type for representing the possible types of Entry - string, number, symbol.
 * 
 * @author ZLAC211
 */
public enum Type {
  STRING("string"), NUMBER("number"), SYMBOL("symbol"), INVALID("INVALID TYPE");

  private String printString;

  Type(String string) {
    printString = string;
  }

  @Override
  public String toString() {
    return printString;
  }

}
