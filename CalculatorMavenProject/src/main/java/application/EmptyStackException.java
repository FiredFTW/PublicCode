package application;
/**
 * Exception thrown when attempting to call pop() or top() on an empty stack.
 * 
 * @author ZLAC211
 */

@SuppressWarnings("serial")
public class EmptyStackException extends Exception {
  /**
   * Creates a new instance of EmptyStackException.
   */
  public EmptyStackException() {
    super("Action cannot be performed on an empty stack");
  }
}
