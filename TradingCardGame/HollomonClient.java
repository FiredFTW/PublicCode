import java.net.*;
import java.io.*;
import java.util.*;


public class HollomonClient{
    String server;
    int port;
    Socket socket;
    InputStream is;
    OutputStream os;
    CardInputStream reader;
    PrintWriter writer;


    public HollomonClient(String server, int port){
        this.server = server;
        this.port = port;
        try{
            //set up streams, reader and writer
            this.socket = new Socket(server, port);
            this.is = socket.getInputStream();
            this.os = socket.getOutputStream();
            this.reader = new CardInputStream(is);
            this.writer = new PrintWriter(os, true);
        } catch (UnknownHostException e){
            System.out.println("Unkown Host Error");
        } catch (IOException e){
            System.out.println("IO Exception");
        }
        
    }

    public List<Card> login(String username, String password){
        
            writer.println(username.toLowerCase());
            writer.println(password);

            if (reader.readResponse().equals("User "+ username +" logged in successfully.")){
                System.out.println("Logged in successfully");
                return readCardList();
            } else {
                System.out.println("unable to log in");
                return null;
            }

    }

    public long getCredits(){
        writer.println("CREDITS");
        long credits = Long.parseLong(reader.readResponse());
        reader.readResponse();
        return credits;
        
    }

    public List<Card> getCards(){
        writer.println("CARDS");
        return readCardList();
    }

    public List<Card> getOffers(){
        writer.println("OFFERS");
        return readCardList();
    } 

    public boolean buyCard(Card card){
        writer.println("BUY " + card.getID());
        return (reader.readResponse().equals("OK"));
    }

    public boolean buyCardID(long id){
        writer.println("BUY " + id);
        return (reader.readResponse().equals("OK"));
    }
    public boolean sellCard(Card card, long price){
        writer.println("SELL "+  card.getID()+" "+price);
        return (reader.readResponse().equals("OK"));
    }


    //functionality for reading a list of cards sent by the server encapsulated in single method
    //as used multiple times
    List<Card> readCardList(){
        ArrayList<Card> cardList = new ArrayList<Card>();
        for(Card card = reader.readCard(); card != null; card = reader.readCard()) {
            cardList.add(card);
        }
        Collections.sort(cardList);
        return cardList;
    }


    public void close(){
        try {
            //close all streams
            socket.close();
            reader.close();
            writer.close();
            is.close();
            os.close();

        } catch (IOException e){
            System.out.println("Unable to close streams.");
        }
        
    }
}