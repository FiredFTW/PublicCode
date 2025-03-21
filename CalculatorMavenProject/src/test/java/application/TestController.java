package application;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import org.junit.jupiter.api.Test;

class TestController {
  private CalcController controller = new CalcController(new CalcModel(), CalcView.getInstance());


  @Test
  void testConstructor() {
    assertNotNull(controller);
  }


}
