package application;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class ReleaseTesting {
  private RevPolishCalc revCalc = new RevPolishCalc();
  private StandardCalc standardCalc = new StandardCalc();


  @Test
  void testNoOperatorsError() {
    assertThrows(InvalidExpression.class, () -> {
      revCalc.evaluate("2 2");
    });
  }

  @Test
  void testLeadingWhiteSpace() {
    try {
      assertEquals(revCalc.evaluate("         1 1 +    "), 2);
    } catch (InvalidExpression e) {

    }

  }
  
  @Test
  void testPostfixInStandard() {
    assertThrows(InvalidExpression.class, () -> {
      standardCalc.evaluate("2 2 +");
    });
  }

 }

