package application;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.fail;
import org.junit.jupiter.api.Test;

class TestStandardCalc {
  StandardCalc calc = new StandardCalc();
  

  @Test
  void test() {
    assertNotNull(calc);
  }
  
  @Test
  void testSimpleCalculation() {
    try {
      assertEquals(calc.evaluate("1 + 1"), 2);
    } catch (InvalidExpression e) {
      fail();
    }
  }
  
  @Test
  void testSimpleCalculation2() {
    try {
      assertEquals(calc.evaluate("1 + 3 * 5"), 16);
    } catch (InvalidExpression e) {
      fail();
    }
  }
  
  @Test
  void testPrecedence() {
    try {
      assertEquals(calc.evaluate("1 / 2 + 5 * 5"), 25.5);
    } catch (InvalidExpression e) {
      fail();
    }
  }
  
  @Test
  void testAllOperators() {
    try {
      assertEquals(calc.evaluate("1 + 3 * 5 - 100 / 10"), 6);
    } catch (InvalidExpression e) {
      fail();
    }
  }
  
  @Test
  void testInvalidExpression() {
    assertThrows(InvalidExpression.class, () -> {
      calc.evaluate("this should fail");
    });
  }
  
  @Test
  void testBrackets() {
    try {
      assertEquals(calc.evaluate("2 * ( 8 + 2 )"), 20);
    } catch (InvalidExpression e) {
      fail();
    }
  }
  
  @Test
  void testDivideByZero() {
    assertThrows(InvalidExpression.class, () -> {
      calc.evaluate("5 0 /");
    });
  }
  
  @Test
  void testEmptyExpression() {
    assertThrows(InvalidExpression.class, () -> {
      calc.evaluate(" ");
    });
  }
  
  @Test
  void testWithCalcModel() {
    CalcModel model = new CalcModel();
    try {
      assertEquals(model.evaluate("3 + 3", OpType.STANDARD), 6);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }
}
