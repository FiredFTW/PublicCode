package application;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class TestSymbol {

  private static Symbol plus;
  private static Symbol minus;
  private static Symbol divide;
  private static Symbol times;
  private static Symbol lbracket;
  private static Symbol rbracket;
  private static Symbol invalid;
  private static Type string;
  private static Type number;
  private static Type symbol;
  private static Type invalidType;

  @BeforeAll // create symbol objects
  static void testConstruction() {
    plus = Symbol.PLUS;
    minus = Symbol.MINUS;
    divide = Symbol.DIVIDE;
    times = Symbol.TIMES;
    lbracket = Symbol.LEFT_BRACKET;
    rbracket = Symbol.RIGHT_BRACKET;
    invalid = Symbol.INVALID;
    string = Type.STRING;
    number = Type.NUMBER;
    symbol = Type.SYMBOL;
    invalidType = Type.INVALID;
  }
  // create symbol and type objects to test


  @Test // test 1
  void testSymbolToString() {
    assertEquals(plus.toString(), "+");
    assertEquals(minus.toString(), "-");
    assertEquals(divide.toString(), "/");
    assertEquals(times.toString(), "*");
    assertEquals(lbracket.toString(), "(");
    assertEquals(rbracket.toString(), ")");
    assertEquals(invalid.toString(), "INVALID SYMBOL");
  }
  // test passed by adding printToken field and toString method
  
  @Test // test 2
  void testTypeToString() {
    assertEquals(number.toString(), "number");
    assertEquals(symbol.toString(), "symbol");
    assertEquals(string.toString(), "string");
    assertEquals(invalidType.toString(), "INVALID TYPE");
   
  }
  // test passed by adding toString method to Type
}
