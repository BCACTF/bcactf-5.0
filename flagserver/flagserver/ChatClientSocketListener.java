package flagserver;

import java.io.ObjectInputStream;

public class ChatClientSocketListener implements Runnable {
    private ObjectInputStream socketIn;

    public ChatClientSocketListener(ObjectInputStream socketIn) {
        this.socketIn = socketIn;
    }

    @Override
    public void run() {
        try {
            while (true) {
                Message msg = (Message) socketIn.readObject();

                if(msg instanceof MessageStoC_Flag){
                    processFlag((MessageStoC_Flag) msg);
                } else {
                    System.out.println("Received unknown message type: " + msg.getClass());
                }
            }
        } catch (Exception ex) {
            System.out.println("Exception caught in listener - " + ex);
        } finally{
            System.out.println("Client Listener exiting");
        }
    }

    private void processFlag(MessageStoC_Flag msg) {
        System.out.println("Flag: " + msg.flag);
    }
}
