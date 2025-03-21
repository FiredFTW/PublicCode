package application;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;


class TestRevPolishCalc {
  private RevPolishCalc calc = new RevPolishCalc();


  @Test
  void testNumberNoCalculation() {
    try {
      assertEquals(calc.evaluate("0"), 0);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }

  @Test
  void testSimpleAddition() {
    try {
      assertEquals(calc.evaluate("1 3 +"), 4);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }

  @Test
  void testSimpleSubtraction() {
    try {
      assertEquals(calc.evaluate("1 1 -"), 0);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }

  @Test
  void testSimpleDivision() {
    try {
      assertEquals(calc.evaluate("4 2 /"), 2);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }


  @Test
  void testSimpleMultiplication() {
    try {
      assertEquals(calc.evaluate("2 3 *"), 6);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }

  @Test
  void testComplexExpression() {
    try {
      assertEquals(calc.evaluate("1 1 + 6 * 0.5 2.5 + /"), 4);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }

  @Test
  void testMultipleSpaces() {
    try {
      assertEquals(calc.evaluate("1   1     +"), 2);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }


  @Test
  void testInvalidExpression() {
    assertThrows(InvalidExpression.class, () -> {
      calc.evaluate("this should fail");
    });
  }

  @Test
  void testDivideByZero() {
    assertThrows(InvalidExpression.class, () -> {
      calc.evaluate("5 0 /");
    });
  }

  @Test
  void testInvalidOperator() {
    assertThrows(InvalidExpression.class, () -> {
      calc.evaluate("1 1 }");
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
      assertEquals(model.evaluate("3 3 +", OpType.REV_POLISH), 6);
    } catch (InvalidExpression e) {
      e.printStackTrace();
    }
  }




}
