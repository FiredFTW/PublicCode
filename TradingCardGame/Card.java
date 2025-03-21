import java.util.*;

public class Card implements Comparable<Object> {
    private long id;
    private String name;
    private Rank rank;
    private long price;
    
    public Card(long id, String name, Rank rank){
        this.id = id;
        this.name = name;
        this.rank = rank;
        this.price = 0;
    }

    public Card(long id, String name, Rank rank, long price){
        this.id = id;
        this.name = name;
        this.rank = rank;
        this.price = price;
    }

    @Override
    public String toString(){
        String output = "";
        output += "Name: " + name + "\n";
        output += "Rarity: " + rank + "\n";
        output += "Price: " + price + "\n";
        output += "ID: " + id + "\n";

        return output;
    }

    @Override
    public boolean equals(Object o){
        if(o == this){
            return true;
        }
        if (!(o instanceof Card)){
            return false;
        }

        Card c = (Card) o;
        return this.id == c.id && this.name.equals(c.name) && this.rank == c.rank;
    }

    @Override
    public int hashCode(){
        //hash id as this should be unique for each seperate card
        return java.util.Objects.hash(id);
    }

     
    public int compareTo(Object o){
        if(o == this){
            return 0;
        }
        if (!(o instanceof Card)){
            return -1;
        }
        Card c = (Card) o;

        //check if rank is then same, then name, then id
        if (this.rank.compareTo(c.rank) != 0){
            return this.rank.compareTo(c.rank);
        }
        if (this.name.compareTo(c.name)!= 0){
            return this.name.compareTo(c.name);
        }
        if (Long.valueOf(this.id).compareTo(Long.valueOf(c.id)) != 0){
            return Long.valueOf(this.id).compareTo(Long.valueOf(c.id));
        }
        return 0;
    }

    public void setPrice(long price){
        this.price = price;
    }

    public long getID(){
        return id;
    }



}