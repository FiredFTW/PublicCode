package application;

/**
 * The controller that sits between the calculator model that does actual evaluation and the view
 * that is the part the user interfaces with.
 * 
 * @author ZLAC211
 */
public class CalcController {
  private CalcModel myModel;
  private ViewInterface myView;
  private OpType calcMode;

  private void handleCalculation() {
    try {
      // fetch expression from GUI textbox, evaluate using correct mode, set answer box to result
      myView.setAnswer(String.valueOf(myModel.evaluate(myView.getExpression(), calcMode)));
    } catch (InvalidExpression e) {
      myView.setAnswer("Invalid Expression!");
    }
  }

  private void handleTypeChange(OpType o) {
    calcMode = o;
  }

  CalcController(CalcModel model, ViewInterface view) {
    myModel = model;
    myView = view;
    calcMode = OpType.STANDARD;

    myView.addCalculateObserver(this::handleCalculation);
    myView.addTypeObserver(this::handleTypeChange);
  }
}
