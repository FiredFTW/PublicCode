package application;

/**
 * Thrown by methods in the Entry class to indicate that requested type is not stored in the object.
 * @author ZLAC211
 */
@SuppressWarnings("serial")
public class BadTypeException extends Exception {
  
  /**
   * Creates a new instance of BadTypeException.
   * 
   * @param message - exception message as a string
   */
  public BadTypeException(String message) {
    super(message);
  }
}
