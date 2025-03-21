package application;

import java.util.Objects;

/**
 * A container class for either a float, string or Symbol.
 * 
 * @author ZLAC211
 */
public class Entry {
  private float number;
  private String str;
  private Symbol other;
  private Type type;
  
  /**
   * Creates a new entry with a float value.
   * 
   * @param value the number to be stored
   */
  public Entry(float value) {
    number = value;
    type = Type.NUMBER;
  }
  
  
  /**
   * Creates a new entry with a string value.
   * 
   * @param string the string to be stored
   */
  public Entry(String string) {
    str = string;
    type = Type.STRING;
  }
  
  /**
   * Creates a new entry with a symbol value.
   * 
   * @param which the symbol to be stored (invalid symbol will create an invalid entry)
   */
  public Entry(Symbol which) {
    other = which;
    // passing an invalid symbol creates an invalid entry
    if (which == Symbol.INVALID) {
      this.type = Type.INVALID;
    } else {
      type = Type.SYMBOL;
    }
  }

  /**
   * Returns the type stored in the entry.
   * 
   * @return enum Type of the stored value
   */
  public Type getType() {
    return type;
  }

  /**
   * Returns the number stored in the entry.
   * 
   * @return float value of number in entry object
   * @throws BadTypeException if the stored entry is not of type float
   */
  public float getValue() throws BadTypeException {
    // check if a number is stored so not to return value that does not exist
    if (type != Type.NUMBER) {
      throw new BadTypeException("Entry does not contain a number value");
    }
    return number;
  }

  /**
   * Returns the string stored in the entry.
   * 
   * @return the string in the entry object
   * @throws BadTypeException if the stored entry is not of type String
   */
  public String getString() throws BadTypeException {
    // check if a string is stored so not to return value that does not exist
    if (type != Type.STRING) {
      throw new BadTypeException("Entry does not contain a string");
    }
    return str;
  }

  /**
   * Returns the symbol stored in the entry.
   * 
   * @return the symbol in the entry object
   * @throws BadTypeException if the stored entry is not of type Symbol
   */
  public Symbol getSymbol() throws BadTypeException {
    // check if a symbol is stored so not to return value that does not exist
    if (type != Type.SYMBOL) {
      throw new BadTypeException("Entry does not contain a symbol");
    }
    return other;
  }

  @Override
  public int hashCode() {
    final int prime = 17; // choose prime number for hashing algorithm
    int hash = 31;
    switch (this.type) {
      case NUMBER:
        // convert float to int as hashcode must return int
        hash = prime * hash + Float.floatToIntBits(number);
        break;
      case STRING:
        hash = prime * hash + this.str.hashCode();
        break;
      case SYMBOL:
        hash = prime * hash + this.other.hashCode();
        break;
      case INVALID: // if type is invalid then use default hashcode method for an object
      default:
        hash = prime * hash + Objects.hashCode(this);
        break;
    }

    return hash;

  }
  
  /**
   * Compares the Entry to another object.
   * 
   * @return TRUE if object is an entry of same type and value, else FALSE
   */
  @Override
  public boolean equals(Object obj) {
    // check if object is being compared to itself
    if (this == obj) {
      return true;
    }

    // check if object is null or is a different class
    if (obj == null || this.getClass() != obj.getClass()) {
      return false;
    }

    Entry otherEntry = (Entry) obj; // cast the object to Entry type

    // check if both entries contain the same type
    if (type != otherEntry.type) {
      return false;
    }

    // compare based on type
    switch (this.type) {
      case NUMBER:
        return Float.compare(otherEntry.number, number) == 0;
      case STRING:
        return Objects.equals(str, otherEntry.str);
      case SYMBOL:
        return Objects.equals(other, otherEntry.other);
      case INVALID:
      default:
        return false;
    }
  }
  
  /**
   * Returns a string representation of the contained value.
   */
  @Override
  public String toString() {
    switch (this.type) {
      case NUMBER:
        return Float.toString(number);
      case STRING:
        return str;
      case SYMBOL:
        return other.toString();
      case INVALID:
      default:
        return "Invalid Entry";
    }
  }



}
